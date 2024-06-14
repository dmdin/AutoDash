export function formatNumber(num: number) {
  const units = ["", "K", "M", "B", "T"];
  let unitIndex = 0;

  while (Math.abs(num) >= 1000 && unitIndex < units.length - 1) {
      num /= 1000;
      unitIndex++;
  }

  let formattedNum = num.toFixed(1);

  if (formattedNum.endsWith('.0')) {
      formattedNum = parseInt(formattedNum);
  }

  return formattedNum + units[unitIndex];
}
