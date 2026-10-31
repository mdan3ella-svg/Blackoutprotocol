import {existsSync,readFileSync,statSync} from 'node:fs';
import {join} from 'node:path';
import {strict as assert} from 'node:assert';
const root=process.cwd();
const html=readFileSync(join(root,'index.html'),'utf8');
for(const file of ['blue.glb','mantaray-XHD.glb','blackoutprotocol.jpg','blackoutprotocol.mp3','vendor/three/three.module.js','vendor/three/addons/loaders/GLTFLoader.js','vendor/three/addons/postprocessing/SSRPass.js','vendor/three/addons/postprocessing/SSAOPass.js']) assert(existsSync(join(root,file)),`Missing: ${file}`);
assert(!/https?:\/\/cdn\.|fonts\.googleapis|fonts\.gstatic/.test(html),'External network reference in HTML');
assert(html.includes('"./vendor/three/three.module.js"'));
assert((html.match(/import \{/g)||[]).length>=8);
for(const file of ['blue.glb','mantaray-XHD.glb']) {
 const b=readFileSync(join(root,file));
 assert.equal(b.toString('ascii',0,4),'glTF');
 assert.equal(b.readUInt32LE(4),2);
 assert.equal(b.readUInt32LE(8),b.length);
 console.log(`VALID GLB ${file} ${b.length} bytes`);
}
console.log('PASS: asset inventory, pinned local imports, GLB headers, and no font/CDN requests in HTML');
