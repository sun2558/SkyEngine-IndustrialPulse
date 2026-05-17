<template>
  <div style="padding: 20px;">
    <h1>天擎工业监控大屏</h1>
    <div ref="chart" style="width: 100%; height: 400px; margin-bottom: 30px;"></div>
    
    <h2>异常列表</h2>
    <div style="max-height: 300px; overflow-y: auto;">
      <table style="width: 100%; border-collapse: collapse;">
        <thead>
          <tr>
            <th style="border: 1px solid #ddd; padding: 8px;">时间</th>
            <th style="border: 1px solid #ddd; padding: 8px;">数值(℃)</th>
            <th style="border: 1px solid #ddd; padding: 8px;">原因</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, index) in anomalies" :key="index">
            <td style="border: 1px solid #ddd; padding: 8px;">{{ item.timestamp }}</td>
            <td style="border: 1px solid #ddd; padding: 8px; color: red;">{{ item.value }}</td>
            <td style="border: 1px solid #ddd; padding: 8px;">{{ item.reason }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
console.log('script 执行了')
import { ref, onMounted } from 'vue'
import * as echarts from 'echarts'
import axios from 'axios'

const chart = ref(null)
const anomalies = ref([])

onMounted(async () => {
  try {
    const res = await axios.get('http://localhost:5000/anomalies')
    anomalies.value = res.data
    console.log('拿到的数据:', res.data)   // 加这一行
    
    // 用异常数据画折线图（这里简化，只把异常点按时间排序画出来）
    const sorted = [...res.data].sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp))
    const chartInstance = echarts.init(chart.value)
    chartInstance.setOption({
      xAxis: { type: 'category', data: sorted.map(p => p.timestamp) },
      yAxis: { type: 'value', name: '温度(℃)' },
      series: [{
        type: 'line',
        data: sorted.map(p => p.value),
        lineStyle: { color: '#409EFF' },
        itemStyle: { color: '#409EFF' }
      }]
    })
  } catch (error) {
    console.error('加载数据失败:', error)
  }
})
</script>

<style scoped>
th, td { text-align: center; }
tr:nth-child(even) { background-color: #f9f9f9; }
</style>