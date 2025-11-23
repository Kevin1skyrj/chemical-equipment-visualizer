import DistributionChart from './charts/DistributionChart'
import SummaryCards from './summary/SummaryCards'
import RecordsTable from './tables/RecordsTable'

const LatestSummary = ({ dataset, isLoading, error }) => {
  if (isLoading) {
    return (
      <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-100 text-center">
        Loading latest dataset…
      </div>
    )
  }

  if (error) {
    return (
      <div className="bg-red-50 p-4 rounded-lg border border-red-200 text-red-800">
        {error}
      </div>
    )
  }

  if (!dataset) {
    return (
      <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-100 text-center text-gray-500">
        Upload a CSV file to see analytics here.
      </div>
    )
  }

  return (
    <section className="bg-white rounded-xl border border-gray-100 shadow-lg p-6 space-y-6">
      <header>
        <p className="text-sm text-gray-500">
          Uploaded on {new Date(dataset.uploaded_at).toLocaleString()}
        </p>
        <h2 className="text-xl font-semibold">{dataset.name}</h2>
      </header>
      <SummaryCards dataset={dataset} />
      <div className="grid lg:grid-cols-2 gap-4">
        <DistributionChart distribution={dataset.type_distribution} />
        <RecordsTable records={dataset.records} />
      </div>
    </section>
  )
}

export default LatestSummary
