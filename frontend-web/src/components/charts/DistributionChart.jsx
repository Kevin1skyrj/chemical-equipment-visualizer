import { useMemo } from 'react'
import { Bar } from 'react-chartjs-2'
import {
  BarElement,
  CategoryScale,
  Chart as ChartJS,
  Legend,
  LinearScale,
  Title,
  Tooltip,
} from 'chart.js'

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend)

const DistributionChart = ({ distribution = {} }) => {
  const chartData = useMemo(() => {
    const labels = Object.keys(distribution)
    const values = Object.values(distribution)
    return {
      labels,
      datasets: [
        {
          label: 'Equipment Count',
          data: values,
          backgroundColor: '#2563eb',
        },
      ],
    }
  }, [distribution])

  const options = {
    responsive: true,
    plugins: {
      legend: { position: 'top' },
      title: { display: true, text: 'Equipment Type Distribution' },
    },
  }

  if (!Object.keys(distribution).length) {
    return (
      <div className="h-full flex items-center justify-center text-gray-500 border border-dashed rounded-lg">
        No distribution data yet.
      </div>
    )
  }

  return (
    <div className="bg-white rounded-lg border border-gray-200 p-4">
      <Bar data={chartData} options={options} height={220} />
    </div>
  )
}

export default DistributionChart
