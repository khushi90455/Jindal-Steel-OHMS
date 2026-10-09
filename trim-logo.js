import sharp from 'sharp';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const inputPath = path.join(__dirname, 'src', 'assets', 'app-icon.png');
const tempPath = path.join(__dirname, 'src', 'assets', 'app-icon-temp.png');

async function trimImage() {
  console.log('Trimming white border from app-icon.png...');
  
  if (!fs.existsSync(inputPath)) {
    console.error('Source image does not exist:', inputPath);
    return;
  }
  
  try {
    // Trim white/off-white background and pad with transparency
    await sharp(inputPath)
      .trim({ background: '#ffffff', threshold: 50 }) // Increased threshold to handle more off-white border shades
      .resize(512, 512, {
        fit: 'contain',
        background: { r: 0, g: 0, b: 0, alpha: 0 } // Clear transparent background
      })
      .png()
      .toFile(tempPath);
      
    // Replace the original source file
    if (fs.existsSync(inputPath)) {
      fs.unlinkSync(inputPath);
    }
    fs.renameSync(tempPath, inputPath);
    console.log('Successfully trimmed white border from app-icon.png!');
  } catch (err) {
    console.error('Error trimming border:', err);
  }
}

trimImage().catch(console.error);
