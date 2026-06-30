function drawBarChart(canvas, { labels, datasets }) {
  const ctx = canvas.getContext("2d");
  const dpr = window.devicePixelRatio || 1;
  const width = canvas.clientWidth || 600;
  const height = canvas.clientHeight || 240;
  canvas.width = width * dpr;
  canvas.height = height * dpr;
  ctx.scale(dpr, dpr);
  ctx.clearRect(0, 0, width, height);

  const paddingLeft = 50;
  const paddingBottom = 30;
  const paddingTop = 20;
  const chartWidth = width - paddingLeft - 20;
  const chartHeight = height - paddingBottom - paddingTop;

  const maxValue = Math.max(
    1,
    ...datasets.flatMap((dataset) => dataset.values)
  );

  const groupCount = labels.length;
  const groupWidth = chartWidth / groupCount;
  const barWidth = (groupWidth * 0.6) / datasets.length;

  ctx.strokeStyle = "#e5e7eb";
  ctx.beginPath();
  ctx.moveTo(paddingLeft, paddingTop);
  ctx.lineTo(paddingLeft, paddingTop + chartHeight);
  ctx.lineTo(paddingLeft + chartWidth, paddingTop + chartHeight);
  ctx.stroke();

  labels.forEach((label, groupIndex) => {
    const groupX = paddingLeft + groupIndex * groupWidth + groupWidth * 0.2;

    datasets.forEach((dataset, datasetIndex) => {
      const value = dataset.values[groupIndex] || 0;
      const barHeight = (value / maxValue) * chartHeight;
      const x = groupX + datasetIndex * barWidth;
      const y = paddingTop + chartHeight - barHeight;

      ctx.fillStyle = dataset.color;
      ctx.fillRect(x, y, barWidth - 4, barHeight);
    });

    ctx.fillStyle = "#6b7280";
    ctx.font = "11px sans-serif";
    ctx.textAlign = "center";
    ctx.fillText(label, groupX + (groupWidth * 0.6) / 2, paddingTop + chartHeight + 16);
  });
}
