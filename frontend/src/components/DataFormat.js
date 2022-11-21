const getRandomColor = (a) => {
  const r = Math.floor(Math.random() * 256);
  const g = Math.floor(Math.random() * 256);
  const b = Math.floor(Math.random() * 256);
  const color = `rgba(${r},${g},${b},${a})`;
  return color;
};

export const DataFormat = (type, inpdata, inplabel, ylabel) => {
  let backgroundColor = getRandomColor(0.2);
  if (type === 'pie') {
    backgroundColor = [];
    for (let i = 0; i < inpdata.length; i += 1) {
      backgroundColor.push(getRandomColor(0.4));
    }
  } return ({
    type,
    data: {
      labels: inplabel,
      datasets: [
        {
          label: ylabel,
          data: inpdata,
          backgroundColor,
          borderColor: getRandomColor(0.5),
        },
      ],
    },
    options: {
      responsive: true,
      scales: {
        yAxes: [{
          scaleLabel: {
            display: true,
            labelString: ylabel,
          },
        }],
        xAxes: [{
          scaleLabel: {
            display: true,
            labelString: 'Date',
          },
        }],
      },
    },
  });
};

export default DataFormat;
