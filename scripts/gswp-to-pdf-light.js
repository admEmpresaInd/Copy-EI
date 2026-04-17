const puppeteer = require('puppeteer');
const path = require('path');

(async () => {
  const outputPath = path.resolve(__dirname, '..', 'EI', 'gswp-book-vendas-light.pdf');
  const url = 'http://localhost:3000/EI/gswp-book-vendas.html';

  console.log('Launching browser (optimized version)...');
  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const page = await browser.newPage();

  // Smaller viewport for lighter rendering
  await page.setViewport({ width: 1280, height: 720, deviceScaleFactor: 1 });

  console.log('Loading page:', url);
  await page.goto(url, {
    waitUntil: 'networkidle0',
    timeout: 30000
  });

  await page.evaluate(() => document.fonts.ready);

  // Force all reveal animations visible
  await page.evaluate(() => {
    document.querySelectorAll('.reveal').forEach(el => el.classList.add('visible'));
    const heroBg = document.getElementById('heroBg');
    if (heroBg) heroBg.classList.add('loaded');
    document.querySelectorAll('[style*="opacity: 0"], [style*="opacity:0"]').forEach(el => {
      el.style.opacity = '1';
      el.style.transform = 'none';
    });

    // Downscale background images to reduce PDF size
    document.querySelectorAll('*').forEach(el => {
      const bg = getComputedStyle(el).backgroundImage;
      if (bg && bg.includes('url(') && bg.includes('/fotos/')) {
        el.style.imageRendering = 'auto';
      }
    });
  });

  await new Promise(r => setTimeout(r, 2000));

  await page.addStyleTag({
    content: `
      @page {
        size: A4 landscape;
        margin: 0;
      }
      .nav, .nav-mobile-toggle, footer { display: none !important; }
      html { scroll-behavior: auto !important; }
      body {
        overflow: visible !important;
        background-color: #1A1917 !important;
      }
      .reveal {
        opacity: 1 !important;
        transform: none !important;
        transition: none !important;
      }
      .hero-label, .hero-title, .hero-subtitle, .hero-details {
        opacity: 1 !important;
        transform: none !important;
        animation: none !important;
      }
      .hero {
        height: 210mm !important;
        min-height: 210mm !important;
        page-break-after: always;
        break-after: page;
      }
      section {
        page-break-inside: avoid;
        break-inside: avoid;
      }
      .about-section,
      .gallery-section,
      .features-section,
      .specs-section,
      .location-section,
      .gswp-section,
      .cta-section {
        page-break-before: always;
        break-before: page;
        min-height: auto;
        padding-top: 3rem;
        padding-bottom: 3rem;
      }
      * {
        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
        color-adjust: exact !important;
      }
      .contact-form { display: none !important; }
      .gallery-grid {
        grid-template-columns: repeat(3, 1fr) !important;
      }
    `
  });

  await new Promise(r => setTimeout(r, 500));

  console.log('Generating optimized PDF...');
  await page.pdf({
    path: outputPath,
    format: 'A4',
    landscape: true,
    printBackground: true,
    preferCSSPageSize: true,
    margin: { top: 0, right: 0, bottom: 0, left: 0 },
    scale: 0.9
  });

  console.log('PDF saved to:', outputPath);

  await browser.close();
  console.log('Done!');
})().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
