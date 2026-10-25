// Рисува редицата със звезди (същата форма като на картата в Wallet).
const STAR = 'M50 4l13.5 29.6 32.4 3.6-24.2 21.9 6.8 31.9L50 74.7 21.5 91l6.8-31.9L4.1 37.2l32.4-3.6z';

export function renderStars(el, stamps, total = 5) {
  el.innerHTML = Array.from(
    { length: total },
    (_, i) => `<svg viewBox="0 0 100 100" aria-hidden="true"><path class="${i < stamps ? 'on' : 'off'}" d="${STAR}"/></svg>`,
  ).join('');
  el.setAttribute('aria-label', `${stamps} of ${total} stars`);
}
