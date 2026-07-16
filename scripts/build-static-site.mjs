import { cp, mkdir, rm, writeFile } from 'node:fs/promises';
import { resolve } from 'node:path';

const root = resolve('.');
const sourceDir = resolve(root, 'docs');
const distDir = resolve(root, 'dist');
const siteDir = resolve(distDir, 'site');
const serverDir = resolve(distDir, 'server');
const hostingDir = resolve(distDir, '.openai');

const serverSource = `
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const siteRoot = path.resolve(__dirname, '..', 'site');
const port = Number(process.env.PORT || 3000);

const contentTypes = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'application/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.svg': 'image/svg+xml',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.gif': 'image/gif',
  '.ico': 'image/x-icon',
  '.txt': 'text/plain; charset=utf-8'
};

function safeResolve(urlPath) {
  const cleanPath = decodeURIComponent(new URL(urlPath, 'http://localhost').pathname);
  const normalized = cleanPath === '/' ? '/index.html' : cleanPath;
  const filePath = path.resolve(siteRoot, '.' + normalized);
  return filePath.startsWith(siteRoot) ? filePath : null;
}

function sendFile(res, filePath) {
  const ext = path.extname(filePath).toLowerCase();
  const type = contentTypes[ext] || 'application/octet-stream';
  res.writeHead(200, { 'Content-Type': type });
  fs.createReadStream(filePath).pipe(res);
}

const server = http.createServer((req, res) => {
  const filePath = safeResolve(req.url || '/');
  if (!filePath) {
    res.writeHead(400);
    res.end('Bad request');
    return;
  }

  if (fs.existsSync(filePath) && fs.statSync(filePath).isFile()) {
    sendFile(res, filePath);
    return;
  }

  const fallback = path.join(siteRoot, 'index.html');
  if (fs.existsSync(fallback)) {
    sendFile(res, fallback);
    return;
  }

  res.writeHead(404);
  res.end('Not found');
});

server.listen(port, () => {
  console.log('Static site server listening on port ' + port);
});
`.trimStart();

await rm(distDir, { recursive: true, force: true });
await mkdir(siteDir, { recursive: true });
await mkdir(serverDir, { recursive: true });
await mkdir(hostingDir, { recursive: true });

await cp(sourceDir, siteDir, { recursive: true });
await cp(resolve(root, '.openai', 'hosting.json'), resolve(hostingDir, 'hosting.json'));
await writeFile(resolve(serverDir, 'index.js'), serverSource, 'utf-8');

console.log(`Prepared deployable output in ${distDir}`);
