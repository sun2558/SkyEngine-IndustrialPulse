<template>
  <div>
    <h1>天擎工业监控大屏</h1>
    <div ref="chart" style="width: 100%; height: 400px;"></div>
    <h2>异常列表</h2>
    <ul>
      <li v-for="(item, index) in anomalies" :key="index">
        {{ item.timestamp }} - {{ item.value }}℃ - {{ item.reason }}
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import * as echarts from 'echarts'
import { getMockData } from './mock.js'

const chart = ref(null)
const anomalies = ref([])

onMounted(() => {
  const data = getMockData()
  anomalies.value = data.anomalies
  
  // 合并正常数据和异常数据用于画图
  const allPoints = [...data.normalData, ...data.anomalies.map(a => ({
    timestamp: a.timestamp,
    value: a.value
  }))]
  
  const chartInstance = echarts.init(chart.value)
  chartInstance.setOption({
    xAxis: { type: 'category', data: allPoints.map(p => p.timestamp) },
    yAxis: { type: 'value', name: '温度(℃)' },
    series: [{
      type: 'line',
      data: allPoints.map(p => p.value),
      markPoint: {
        data: data.anomalies.map(a => ({ coord: [a.timestamp, a.value], value: a.value }))
      }
    }]
  })
})
</script>