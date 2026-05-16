// src/mock.js
export const getMockData = () => {
  return {
    anomalies: [
      { timestamp: '2026-05-16 08:23:00', value: 88.5, reason: '温度超过正常范围' },
      { timestamp: '2026-05-16 09:47:00', value: 92.3, reason: '温度超过正常范围' },
      { timestamp: '2026-05-16 11:02:00', value: 85.9, reason: '温度超过正常范围' },
      { timestamp: '2026-05-16 13:34:00', value: 95.1, reason: '温度超过正常范围' },
      { timestamp: '2026-05-16 15:18:00', value: 89.7, reason: '温度超过正常范围' }
    ],
    normalData: [
      { timestamp: '2026-05-16 08:00:00', value: 22.5 },
      { timestamp: '2026-05-16 09:00:00', value: 23.1 },
      { timestamp: '2026-05-16 10:00:00', value: 24.8 },
      { timestamp: '2026-05-16 11:00:00', value: 23.9 },
      { timestamp: '2026-05-16 12:00:00', value: 25.2 },
      { timestamp: '2026-05-16 13:00:00', value: 24.6 },
      { timestamp: '2026-05-16 14:00:00', value: 26.1 },
      { timestamp: '2026-05-16 15:00:00', value: 25.8 }
    ]
  }
}