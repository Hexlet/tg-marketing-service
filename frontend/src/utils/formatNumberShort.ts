function formatNumberShort(num: number): string {
  if (num >= 1_000_000) {
    return (num / 1_000_000).toFixed(1).replace(/\.0$/, '') + ' млн';
  } else if (num >= 10_000) {
    return Math.round(num / 1_000) + ' тыс.';
  } else if (num >= 1_000) {
    return (num / 1_000).toFixed(1).replace(/\.0$/, '') + ' тыс.';
  } else {
    return num.toString();
  }
}

export default formatNumberShort;
