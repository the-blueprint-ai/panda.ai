<script>
import { DateTime } from "luxon";
import { Bar } from "vue-chartjs";
import { generateDateRange } from "../composables/generateDateRange.js";
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
  props: {
    dataByDay: {
      type: Object,
      required: true,
    },
    axisName: String,
  },
  data() {
    return {
      chartData: {
        labels: [],
        datasets: [
          {
            label: "Test Data",
            barThickness: 10,
            backgroundColor: "#FFCB4C",
            hoverBackgroundColor: "#FFFFFF",
            borderColor: "#FFCB4C",
            borderRadius: 20,
            hoverBorderColor: "#000000",
            borderWidth: 1,
            data: [],
          },
        ],
      },
      plugins: ["plugin"],
      chartOptions: {
        aspectRatio: 4,
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
            title: {
              display: false,
              text: "",
              padding: 16,
              font: {
                family: "Monaco",
                size: 18,
              },
            },
            // display: false,
            grid: {
              display: false,
            },
            ticks: {
              stepSize: 1,
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
  watch: {
    dataByDay: {
      immediate: true,
      handler(newData) {
        if (newData) {
          const startDate = DateTime.fromISO(newData[0].date);
          const endDate = DateTime.fromISO(newData[newData.length - 1].date);
          const dateRange = generateDateRange(startDate, endDate);

          this.chartData.labels = dateRange.map((date) =>
            date.toFormat("dd-MM-yyyy")
          );
          this.chartData.datasets[0].data = dateRange.map((date) => {
            const foundData = newData.find(
              (item) =>
                DateTime.fromISO(item.date).toFormat("dd-MM-yyyy") ===
                date.toFormat("dd-MM-yyyy")
            );
            return foundData ? foundData.volume : 0;
          });
        } else {
          this.chartData.labels = [];
          this.chartData.datasets[0].data = [];
        }
      },
    },
    axisName: {
      immediate: true,
      handler(newData) {
        if (newData) {
          this.chartOptions.scales.y.title.text = newData;
        } else {
          this.chartOptions.scales.y.title.text = "";
        }
      },
    },
  },
  computed: {},
  components: { Bar },
};
</script>

<template>
  <Bar id="my-chart-id" :options="chartOptions" :data="chartData" />
</template>
