// Miles Run Tracker - Rolling number wheel
document.addEventListener('DOMContentLoaded', function() {
  const MILES_RUN = 1161.4;
  const PLACEHOLDER_CHAR = '🍞';
  const PLACEHOLDER_PAUSE = 1200;
  const DIGIT_HEIGHT = 56;
  const positions = ['thousands', 'hundreds', 'tens', 'ones', 'tenths'];

  function createDigitStrip(cycles = 8) {
    const strip = [];      
    strip.push(`<span>${PLACEHOLDER_CHAR}</span>`);
    for (let c = 0; c < cycles; c++) {
      for (let i = 0; i <= 9; i++) {
        strip.push(`<span>${i}</span>`);
      }
    }
    return strip.join('');
  }

  function initWheels() {
    positions.forEach(pos => {
      const wheel = document.querySelector(`.digit-wheel[data-position="${pos}"]`);
      if (wheel) {
        const strip = wheel.querySelector('.digit-strip');
        strip.innerHTML = createDigitStrip();
        strip.style.transform = 'translateY(0)';
      }
    });
  }

  function getTranslateY(digit) {
    return -(digit + 1) * DIGIT_HEIGHT;
  }

  function formatMiles(value) {
    const str = Math.min(99999.9, Math.max(0, value)).toFixed(1);
    const [whole, dec] = str.split('.');
    const padded = whole.padStart(4, '0');
    return [...padded, dec].map(Number);
  }

  function runStartAnimation() {
    const digitEls = positions.map(pos => document.querySelector(`.digit-wheel[data-position="${pos}"]`)).filter(Boolean);
    const targetDigits = formatMiles(MILES_RUN);

    digitEls.forEach((wheel) => {
      const strip = wheel.querySelector('.digit-strip');
      wheel.classList.add('spinning');
      strip.style.transition = 'none';
      strip.style.transform = 'translateY(0)';
    });

    const stopOrder = [4, 3, 2, 1, 0];
    const stopDelay = 320;

    stopOrder.forEach((wheelIndex, order) => {
      setTimeout(() => {
        const wheel = digitEls[wheelIndex];
        if (!wheel) return;
        const strip = wheel.querySelector('.digit-strip');
        wheel.classList.remove('spinning');
        strip.style.transition = 'transform 0.7s cubic-bezier(0.34, 1.56, 0.64, 1)';
        strip.style.transform = `translateY(${getTranslateY(targetDigits[wheelIndex])}px)`;
        setTimeout(() => { strip.style.transition = ''; }, 700);
      }, order * stopDelay);
    });
  }

  function init() {
    initWheels();
    setTimeout(runStartAnimation, PLACEHOLDER_PAUSE);
  }

  init();

  // Typing hero title — reserve layout (no jump in content below)
  const pageTitle = document.querySelector('.hero-title');
  if (pageTitle) {
    const text = pageTitle.textContent.trim();
    if (!text.length) {
      /* skip */
    } else {
      pageTitle.setAttribute('aria-label', text);
      pageTitle.textContent = '';
      pageTitle.classList.add('hero-title-typewriter');

      const slot = document.createElement('span');
      slot.className = 'hero-title-typewriter-slot';

      const measure = document.createElement('span');
      measure.className = 'hero-title-typewriter-measure';
      measure.setAttribute('aria-hidden', 'true');
      measure.textContent = text;

      const typed = document.createElement('span');
      typed.className = 'hero-title-typewriter-typed';

      slot.appendChild(measure);
      slot.appendChild(typed);
      pageTitle.appendChild(slot);

      let i = 0;
      const typeWriter = () => {
        if (i < text.length) {
          typed.textContent += text.charAt(i);
          i++;
          setTimeout(typeWriter, 100);
        }
      };

      setTimeout(typeWriter, 500);
    }
  }

  const lightningRain = document.querySelector('.lightning-rain');
  if (
    lightningRain &&
    !window.matchMedia('(prefers-reduced-motion: reduce)').matches
  ) {
    const count = 30;
    const frag = document.createDocumentFragment();
    for (let i = 0; i < count; i++) {
      const el = document.createElement('span');
      el.className = 'lightning-drop';
      el.textContent = '\u26A1';
      el.setAttribute('aria-hidden', 'true');
      el.style.left = `${Math.random() * 100}%`;
      el.style.animationDuration = `${4 + Math.random() * 6}s`;
      el.style.animationDelay = `${-Math.random() * 12}s`;
      el.style.fontSize = `${1.35 + Math.random() * 1.1}rem`;
      frag.appendChild(el);
    }
    lightningRain.appendChild(frag);
  }
});
