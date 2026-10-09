import sharp from 'sharp';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import pngToIco from 'png-to-ico';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const svgContent = `
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <defs>
    <!-- Background Gradient -->
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0a0f1d" />
      <stop offset="100%" stop-color="#141a29" />
    </linearGradient>

    <!-- Medical/Teal Gradient -->
    <linearGradient id="primaryGrad" x1="0%" y1="100%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#06b6d4" />
      <stop offset="100%" stop-color="#3b82f6" />
    </linearGradient>

    <!-- Steel/Silver Gradient -->
    <linearGradient id="steelGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#f8fafc" />
      <stop offset="50%" stop-color="#cbd5e1" />
      <stop offset="100%" stop-color="#64748b" />
    </linearGradient>

    <!-- Glow Filter -->
    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="12" result="blur" />
      <feMerge>
        <feMergeNode in="blur" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>

    <!-- Soft Glow Filter -->
    <filter id="softGlow" x="-10%" y="-10%" width="120%" height="120%">
      <feGaussianBlur stdDeviation="6" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>
  </defs>

  <!-- Rounded Background Container -->
  <rect width="512" height="512" rx="110" fill="url(#bgGrad)" stroke="url(#steelGrad)" stroke-width="3" />

  <!-- Subtle Inner Ring/Accent -->
  <rect x="25" y="25" width="462" height="462" rx="88" fill="none" stroke="#ffffff" stroke-opacity="0.03" stroke-width="2" />

  <!-- Outer Glowing Steel Ring (Industrial) -->
  <circle cx="256" cy="230" r="135" fill="none" stroke="url(#steelGrad)" stroke-width="12" stroke-dasharray="10 15 25 15" opacity="0.3" transform="rotate(-45 256 230)" />
  <circle cx="256" cy="230" r="135" fill="none" stroke="url(#primaryGrad)" stroke-width="4" opacity="0.5" filter="url(#softGlow)" />

  <!-- The Vertical Bars of the Medical Cross (Clean Rounded Pills) -->
  <!-- Top Arm -->
  <rect x="238" y="115" width="36" height="65" rx="18" fill="url(#steelGrad)" />
  <!-- Bottom Arm -->
  <rect x="238" y="280" width="36" height="65" rx="18" fill="url(#steelGrad)" />

  <!-- The Horizontal Pulse Wave (representing the medical cross horizontal bar & heartbeat) -->
  <path d="M 120 230 L 195 230 L 210 200 L 225 295 L 245 145 L 265 265 L 280 215 L 295 240 L 310 230 L 392 230" 
        fill="none" 
        stroke="url(#primaryGrad)" 
        stroke-width="14" 
        stroke-linecap="round" 
        stroke-linejoin="round" 
        filter="url(#glow)" />

  <!-- Glowing Pulse Nodes -->
  <circle cx="245" cy="145" r="7" fill="#ffffff" filter="url(#softGlow)" />
  <circle cx="225" cy="295" r="7" fill="#ffffff" filter="url(#softGlow)" />

  <!-- Label/Text for JSPulse -->
  <text x="256" y="415" 
        font-family="'Inter', 'Outfit', 'Segoe UI', system-ui, sans-serif" 
        font-weight="900" 
        font-size="34" 
        fill="url(#steelGrad)" 
        text-anchor="middle" 
        letter-spacing="4">
    JS<tspan fill="#06b6d4">PULSE</tspan>
  </text>

  <!-- Sub-label/Text for OHMS -->
  <text x="256" y="452" 
        font-family="'Inter', 'Outfit', 'Segoe UI', system-ui, sans-serif" 
        font-weight="700" 
        font-size="20" 
        fill="#94a3b8" 
        text-anchor="middle" 
        letter-spacing="8" 
        opacity="0.8">
    OHMS
  </text>
</svg>
`;

// Paths to output files
const buildDir = path.join(__dirname, 'build');
if (!fs.existsSync(buildDir)) {
  fs.mkdirSync(buildDir);
}

const paths = {
  srcIcon: path.join(__dirname, 'src', 'assets', 'app-icon.png'),
  buildIcon: path.join(buildDir, 'icon.png'),
  publicLogo: path.join(__dirname, 'public', 'logo.png'),
  artifactSvg: 'C:/Users/ashwi/.gemini/antigravity/brain/befed194-fe3f-45e5-8976-b84c908cf4b6/jspulse_ohms_premium_logo.svg',
  artifactPng: 'C:/Users/ashwi/.gemini/antigravity/brain/befed194-fe3f-45e5-8976-b84c908cf4b6/jspulse_ohms_premium_logo.png'
};

async function main() {
  console.log('Generating premium SVG & PNG logos...');

  // Save SVG artifact
  fs.writeFileSync(paths.artifactSvg, svgContent);
  console.log('Saved SVG artifact to:', paths.artifactSvg);

  const svgBuffer = Buffer.from(svgContent);

  // Render high-res PNG for various outputs
  await sharp(svgBuffer)
    .resize(512, 512)
    .png()
    .toFile(paths.srcIcon);
  console.log('Saved source icon to:', paths.srcIcon);

  await sharp(svgBuffer)
    .resize(256, 256)
    .png()
    .toFile(paths.buildIcon);
  console.log('Saved build icon to:', paths.buildIcon);

  await sharp(svgBuffer)
    .resize(256, 256)
    .png()
    .toFile(paths.publicLogo);
  console.log('Saved public logo to:', paths.publicLogo);

  await sharp(svgBuffer)
    .resize(512, 512)
    .png()
    .toFile(paths.artifactPng);
  console.log('Saved PNG artifact to:', paths.artifactPng);

  // Generate ICO file
  console.log('Converting build/icon.png to build/icon.ico...');
  try {
    const fn = pngToIco.default || pngToIco;
    const icoBuf = await fn(paths.buildIcon);
    fs.writeFileSync(path.join(buildDir, 'icon.ico'), icoBuf);
    console.log('Successfully created build/icon.ico');
  } catch (icoErr) {
    console.error('Failed to convert to ICO:', icoErr);
  }

  console.log('All branding assets successfully generated!');
}

main().catch(console.error);
