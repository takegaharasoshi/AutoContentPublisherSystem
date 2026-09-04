import fs from 'node:fs';
import zlib from 'node:zlib';

const [input, output] = process.argv.slice(2);
const source = fs.readFileSync(input);
if (source.toString('ascii', 1, 4) !== 'PNG') throw new Error('Expected PNG');

let position = 8;
let width, height, bitDepth, colorType;
const idat = [];
while (position < source.length) {
  const size = source.readUInt32BE(position); position += 4;
  const kind = source.toString('ascii', position, position + 4); position += 4;
  const body = source.subarray(position, position + size); position += size + 4;
  if (kind === 'IHDR') {
    width = body.readUInt32BE(0); height = body.readUInt32BE(4);
    bitDepth = body[8]; colorType = body[9];
  } else if (kind === 'IDAT') idat.push(body);
}
if (bitDepth !== 8 || colorType !== 2) throw new Error('Expected 8-bit RGB PNG');

const raw = zlib.inflateSync(Buffer.concat(idat));
const rgb = Buffer.alloc(width * height * 3);
const stride = width * 3;
let previous = Buffer.alloc(stride);
let offset = 0;
for (let y = 0; y < height; y++) {
  const filter = raw[offset++];
  const row = Buffer.from(raw.subarray(offset, offset + stride)); offset += stride;
  for (let x = 0; x < stride; x++) {
    const left = x >= 3 ? row[x - 3] : 0;
    const up = previous[x];
    const upLeft = x >= 3 ? previous[x - 3] : 0;
    if (filter === 1) row[x] = (row[x] + left) & 255;
    else if (filter === 2) row[x] = (row[x] + up) & 255;
    else if (filter === 3) row[x] = (row[x] + Math.floor((left + up) / 2)) & 255;
    else if (filter === 4) {
      const p = left + up - upLeft;
      const pa = Math.abs(p - left), pb = Math.abs(p - up), pc = Math.abs(p - upLeft);
      row[x] = (row[x] + (pa <= pb && pa <= pc ? left : pb <= pc ? up : upLeft)) & 255;
    } else if (filter !== 0) throw new Error(`Unsupported filter ${filter}`);
  }
  row.copy(rgb, y * stride); previous = row;
}

const rgba = new Uint8Array(width * height * 4);
for (let i = 0, j = 0; i < rgb.length; i += 3, j += 4) {
  const r = rgb[i], g = rgb[i + 1], b = rgb[i + 2];
  const distance = Math.hypot(r - 255, g, b - 255);
  const alpha = Math.max(0, Math.min(255, Math.round((distance - 55) * 255 / 65)));
  rgba[j + 3] = alpha;
  if (alpha) {
    const a = alpha / 255;
    rgba[j] = Math.max(0, Math.min(255, Math.round((r - (1 - a) * 255) / a)));
    rgba[j + 1] = Math.max(0, Math.min(255, Math.round(g / a)));
    rgba[j + 2] = Math.max(0, Math.min(255, Math.round((b - (1 - a) * 255) / a)));
  }
}

const outSize = 1024;
const resized = new Uint8Array(outSize * outSize * 4);
for (let y = 0; y < outSize; y++) for (let x = 0; x < outSize; x++) {
  const sx = Math.min(width - 1, Math.floor((x + 0.5) * width / outSize));
  const sy = Math.min(height - 1, Math.floor((y + 0.5) * height / outSize));
  const s = (sy * width + sx) * 4, d = (y * outSize + x) * 4;
  resized[d] = rgba[s]; resized[d + 1] = rgba[s + 1]; resized[d + 2] = rgba[s + 2]; resized[d + 3] = rgba[s + 3];
}

const crcTable = Uint32Array.from({length: 256}, (_, n) => {
  let c = n;
  for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1;
  return c >>> 0;
});
const crc32 = buffer => {
  let c = 0xffffffff;
  for (const byte of buffer) c = crcTable[(c ^ byte) & 255] ^ (c >>> 8);
  return (c ^ 0xffffffff) >>> 0;
};
const chunk = (kind, body) => {
  const name = Buffer.from(kind), result = Buffer.alloc(body.length + 12);
  result.writeUInt32BE(body.length, 0); name.copy(result, 4); body.copy(result, 8);
  result.writeUInt32BE(crc32(Buffer.concat([name, body])), body.length + 8);
  return result;
};
const scanlines = Buffer.alloc(outSize * (outSize * 4 + 1));
for (let y = 0; y < outSize; y++) {
  const at = y * (outSize * 4 + 1); scanlines[at] = 0;
  Buffer.from(resized.subarray(y * outSize * 4, (y + 1) * outSize * 4)).copy(scanlines, at + 1);
}
const header = Buffer.alloc(13); header.writeUInt32BE(outSize, 0); header.writeUInt32BE(outSize, 4); header[8] = 8; header[9] = 6;
fs.writeFileSync(output, Buffer.concat([Buffer.from([137,80,78,71,13,10,26,10]), chunk('IHDR', header), chunk('IDAT', zlib.deflateSync(scanlines, {level: 9})), chunk('IEND', Buffer.alloc(0))]));
