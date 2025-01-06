const fs = require("fs");
const path = require("path");
const { createCanvas, loadImage } = require("canvas");
const NMO_AmbientOccMap = require("./ambientOccMap");

async function processImage(inputPath, outputPath) {
  // Load the input image
  const heightImage = await loadImage(inputPath);
  const width = heightImage.width;
  const height = heightImage.height;

  // Initialize AO map object
  const AO = NMO_AmbientOccMap;
  AO.ao_canvas = createCanvas(width, height);

  // Set AO parameters as desired
  AO.height_image = heightImage;
  AO.ao_range = 1;
  AO.ao_strength = 0.5;
  AO.ao_mean = 1;
  AO.ao_smoothing = 0; // no blur/sharpen for now
  AO.invert_ao = false; // not inverted by default
  // If using CPU method from code comments, ensure you have that code active and GPU code disabled.

  // Draw height image onto AO canvas
  const ctx = AO.ao_canvas.getContext("2d");
  ctx.drawImage(heightImage, 0, 0, width, height);

  // Initialize AO shader
  AO.initAOshader();
  // Run AO generation (assuming you've adapted CPU-based method)
  AO.createAmbientOcclusionTexture();

  fs.mkdirSync(path.dirname(outputPath), { recursive: true });

  const outStream = fs.createWriteStream(outputPath);
  const stream = AO.ao_canvas.createPNGStream();
  stream.pipe(outStream);
  return new Promise((resolve, reject) => {
    outStream.on("finish", () => {
      console.log(`AO map saved to ${outputPath}`);
      resolve();
    });
    outStream.on("error", reject);
  });
}

async function runForAllImages() {
  // const inputDir = path.join(__dirname, "..", "inputs");
  const inputDir = path.join(__dirname, "..", "..", "..", "Inputs");

  // const outputDir = path.join(__dirname, "..", "outputs");
  const outputDir = path.join(__dirname, "..", "..", "..", "Outputs", "OcclusionMaps");

  const imagePaths = readImagesRecursively(inputDir);
  for (const inputPath of imagePaths) {
    const relativePath = path.relative(inputDir, inputPath);
    const baseName = path.parse(relativePath).name;
    const outputSubDir = path.dirname(relativePath);
    const outputPath = path.join(outputDir, outputSubDir, `${baseName}/${baseName}-nmo.png`);

    try {
      await processImage(inputPath, outputPath);
    } catch (error) {
      console.error(`Failed to process ${inputPath}:`, error);
    }
  }

  console.log("All images processed.");
}

function readImagesRecursively(dir) {
  let imagePaths = [];
  const entries = fs.readdirSync(dir, { withFileTypes: true });

  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      // Recursively read subdirectories
      imagePaths = imagePaths.concat(readImagesRecursively(fullPath));
    } else if (entry.isFile()) {
      // Check if file is an image
      const ext = path.extname(entry.name).toLowerCase();
      if ([".png", ".jpg", ".jpeg", ".tiff"].includes(ext)) {
        imagePaths.push(fullPath);
      }
    }
  }

  return imagePaths;
}

runForAllImages().catch((err) => console.error(err));
