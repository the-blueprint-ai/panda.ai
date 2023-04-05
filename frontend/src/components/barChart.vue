<script>
import { Bar } from "vue-chartjs";
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
} from "chart.js";
ChartJS.register(
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale
);

export default {
  name: "BarChart",
  data() {
    return {
      chartData: {
        labels: ["January", "February", "March"],
        datasets: [
          {
            label: "Test Data",
            backgroundColor: "#FFCB4C",
            hoverBackgroundColor: "#FFFFFF",
            // borderColor: "#FFFFFF",
            hoverBorderColor: "#000000",
            borderWidth: 1,
            data: [40, 20, 12],
          },
        ],
      },
      plugins: ["plugin"],
      chartOptions: {
        scales: {
          x: {
            // display: false,
            grid: {
              display: false,
            },
            ticks: {
              // display: false,
            },
          },
          y: {
            // display: false,
            grid: {
              display: false,
            },
            ticks: {
              // display: false,
            },
          },
        },
        responsive: true,
        plugins: {
          legend: {
            display: false,
          },
          tooltip: {
            enabled: false,
          },
        },
      },
    };
  },
  components: { Bar },
  computed: {},
};
</script>

<template>
  <Bar id="my-chart-id" :options="chartOptions" :data="chartData" />
</template>
