import sharp from 'sharp';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const srcImage = path.join(__dirname, 'src', 'assets', 'app-icon.png');
const buildDir = path.join(__dirname, 'build');
const pngPath = path.join(buildDir, 'icon.png');
const publicPngPath = path.join(__dirname, 'public', 'logo.png');

if (!fs.existsSync(buildDir)) {
  fs.mkdirSync(buildDir);
}

// Generate build icon (256x256 for electron-builder)
sharp(srcImage)
  .resize(256, 256, { fit: 'cover' })
  .png()
  .toFile(pngPath)
  .then(() => {
    console.log('Successfully generated icon at', pngPath);
    
    // Generate public/logo.png (for browser tab)
    return sharp(srcImage)
      .resize(256, 256, { fit: 'cover' })
      .png()
      .toFile(publicPngPath);
  })
  .then(() => console.log('Successfully generated logo at', publicPngPath))
  .catch(err => console.error('Error generating icon:', err));
