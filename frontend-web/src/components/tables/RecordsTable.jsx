const RecordsTable = ({ records = [] }) => {
  if (!records.length) {
    return (
      <div className="border border-dashed border-gray-300 rounded-lg p-4 text-center text-gray-500">
        No records available.
      </div>
    )
  }

  const columns = Object.keys(records[0])
  const visibleRecords = records.slice(0, 50)

  return (
    <div className="overflow-auto border border-gray-200 rounded-lg">
      <table className="min-w-full text-sm">
        <thead className="bg-gray-50">
          <tr>
            {columns.map((column) => (
              <th key={column} className="px-4 py-2 text-left font-semibold text-gray-600">
                {column.replace('_', ' ')}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {visibleRecords.map((record, index) => (
            <tr key={`${record.equipment_name}-${index}`} className="odd:bg-white even:bg-gray-50">
              {columns.map((column) => (
                <td key={column} className="px-4 py-2 text-gray-700">
                  {record[column]}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
      {records.length > visibleRecords.length && (
        <p className="text-xs text-gray-500 px-4 py-2">
          Showing {visibleRecords.length} of {records.length} rows.
        </p>
      )}
    </div>
  )
}

export default RecordsTable
