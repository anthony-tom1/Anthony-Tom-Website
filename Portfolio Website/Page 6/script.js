// Miles Run Tracker - Rolling number wheel
document.addEventListener('DOMContentLoaded', function() {
  const MILES_RUN = 956.4;
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

  // Typing effect for hero title (same as other pages)
  const pageTitle = document.querySelector('.hero-title');
  if (pageTitle) {
    const text = pageTitle.textContent.trim();
    pageTitle.textContent = '';

    let i = 0;
    const typeWriter = () => {
      if (i < text.length) {
        pageTitle.textContent += text.charAt(i);
        i++;
        setTimeout(typeWriter, 100);
      }
    };

    setTimeout(typeWriter, 500);
  }
});
