// Presentation only: an empty assessment is not a measurement of no effect.
export function impactCount(event) {
  if (Array.isArray(event.impacts)) return event.impacts.length;
  if (Number.isInteger(event.impactCount) && event.impactCount >= 0) return event.impactCount;
  return null;
}

// Summary payloads do not contain full impacts. Never call .some on missing data.
export function impactDimensions(event) {
  if (Array.isArray(event.impacts)) return [...new Set(event.impacts.map(x => x.dimension).filter(Boolean))];
  if (Array.isArray(event.impactDimensions)) return [...new Set(event.impactDimensions.filter(x => typeof x === 'string'))];
  return [];
}

export function impactIndexLabel(event, chinese = false) {
  const count = impactCount(event);
  if (count === 0) return chinese ? '尚无已记录影响' : 'No impacts recorded';
  if (count === null) return chinese ? '影响资料待加载' : 'Impact data pending';
  return Number.isInteger(event.impactIndex) ? `${event.impactIndex}/10` : (chinese ? '待评估' : 'Not assessed');
}

export function impactEmptyMessage(chinese = false) {
  return chinese
    ? '尚未录入可计分的影响条目；不表示实测影响为零，也不表示已经完成影响审计。'
    : 'No scored impact entries have been recorded. This does not establish zero real-world impact or a completed impact audit.';
}
