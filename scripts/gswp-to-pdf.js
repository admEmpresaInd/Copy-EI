const puppeteer = require('puppeteer');
const path = require('path');

(async () => {
  const outputPath = path.resolve(__dirname, '..', 'EI', 'gswp-book-vendas.pdf');
  const url = 'http://localhost:3000/EI/gswp-book-vendas.html';

  console.log('Launching browser...');
  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const page = await browser.newPage();

  // Set viewport to landscape 1920x1080 for proper rendering
  await page.setViewport({ width: 1920, height: 1080 });

  console.log('Loading page:', url);
  await page.goto(url, {
    waitUntil: 'networkidle0',
    timeout: 30000
  });

  // Wait for fonts to load
  await page.evaluate(() => document.fonts.ready);

  // Force all reveal animations to be visible (they rely on IntersectionObserver)
  await page.evaluate(() => {
    document.querySelectorAll('.reveal').forEach(el => {
      el.classList.add('visible');
    });
    // Force hero background loaded state
    const heroBg = document.getElementById('heroBg');
    if (heroBg) heroBg.classList.add('loaded');
    // Force all animated elements to be visible
    document.querySelectorAll('[style*="opacity: 0"], [style*="opacity:0"]').forEach(el => {
      el.style.opacity = '1';
      el.style.transform = 'none';
    });
  });

  // Wait a moment for any CSS transitions
  await new Promise(r => setTimeout(r, 2000));

  // Inject print-optimized CSS for landscape book layout
  await page.addStyleTag({
    content: `
      @page {
        size: A4 landscape;
        margin: 0;
      }

      /* Hide navigation and mobile elements */
      .nav, .nav-mobile-toggle, footer { display: none !important; }

      /* Remove scroll/animation behaviors */
      html { scroll-behavior: auto !important; }
      body {
        overflow: visible !important;
        background-color: #1A1917 !important;
      }

      /* Force all content visible */
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

      /* Hero section as full landscape page */
      .hero {
        height: 210mm !important;
        min-height: 210mm !important;
        page-break-after: always;
        break-after: page;
      }

      /* Each major section gets its own page */
      section {
        page-break-inside: avoid;
        break-inside: avoid;
      }

      /* Sections with enough content get page breaks */
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

      /* Ensure images render properly */
      img {
        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
        color-adjust: exact !important;
      }

      /* Preserve background colors and images */
      * {
        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
        color-adjust: exact !important;
      }

      /* Remove form from CTA section in print */
      .contact-form { display: none !important; }

      /* Adjust gallery grid for landscape */
      .gallery-grid {
        grid-template-columns: repeat(3, 1fr) !important;
      }
    `
  });

  // Wait for styles to apply
  await new Promise(r => setTimeout(r, 500));

  console.log('Generating PDF...');
  await page.pdf({
    path: outputPath,
    format: 'A4',
    landscape: true,
    printBackground: true,
    preferCSSPageSize: true,
    margin: { top: 0, right: 0, bottom: 0, left: 0 }
  });

  console.log('PDF saved to:', outputPath);

  await browser.close();
  console.log('Done!');
})().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
