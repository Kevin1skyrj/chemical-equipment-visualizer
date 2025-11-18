const SummaryCards = ({ dataset }) => {
  const cards = [
    { label: 'Total Records', value: dataset.total_records },
    { label: 'Avg Flowrate', value: `${dataset.avg_flowrate} m3/h` },
    { label: 'Avg Pressure', value: `${dataset.avg_pressure} bar` },
    { label: 'Avg Temperature', value: `${dataset.avg_temperature} °C` },
  ]

  return (
    <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
      {cards.map((card) => (
        <div
          key={card.label}
          className="border border-gray-200 rounded-lg p-4 bg-linear-to-br from-white to-slate-50"
        >
          <p className="text-xs uppercase tracking-wide text-gray-500">
            {card.label}
          </p>
          <p className="text-xl font-semibold mt-2">{card.value}</p>
        </div>
      ))}
    </div>
  )
}

export default SummaryCards
