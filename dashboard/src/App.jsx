import { useState, useEffect } from "react";
import axios from "axios";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";

const API = "http://localhost:8000";

export default function App() {
  const [stats, setStats] = useState(null);
  const [transactions, setTransactions] = useState([]);

  useEffect(() => {
    const fetchData = () => {
      axios.get(`${API}/stats`).then(res => setStats(res.data));
      axios.get(`${API}/transactions?limit=20`).then(res => setTransactions(res.data));
    };
    fetchData();
    const interval = setInterval(fetchData, 3000);
    return () => clearInterval(interval);
  }, []);

  const chartData = transactions.slice().reverse().map((t, i) => ({
    idx: i,
    risk: t.risk_score
  }));

  return (
    <div style={{ background: "#0B0F14", minHeight: "100vh", color: "#E8EDF2", fontFamily: "system-ui", padding: "32px" }}>
      <h1 style={{ fontSize: "28px", fontWeight: 600, marginBottom: "4px" }}>Sentri</h1>
      <p style={{ color: "#7C8B9C", marginBottom: "32px" }}>Real-time fraud detection dashboard</p>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: "16px", marginBottom: "32px" }}>
        <StatCard label="Total Transactions" value={stats?.total_transactions ?? "-"} color="#378ADD" />
        <StatCard label="Fraud Detected" value={stats?.fraud_detected ?? "-"} color="#E24B4A" />
        <StatCard label="Fraud Rate" value={`${stats?.fraud_rate_pct ?? 0}%`} color="#F0A93B" />
        <StatCard label="Avg Risk Score" value={`${stats?.average_risk_score ?? 0}%`} color="#34C77B" />
      </div>

      <div style={{ background: "#141A22", borderRadius: "12px", padding: "20px", marginBottom: "32px" }}>
        <h3 style={{ marginBottom: "16px", color: "#A8B5C2" }}>Risk Score Trend (last 20 transactions)</h3>
        <ResponsiveContainer width="100%" height={220}>
          <LineChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#222A33" />
            <XAxis dataKey="idx" stroke="#7C8B9C" />
            <YAxis stroke="#7C8B9C" />
            <Tooltip contentStyle={{ background: "#1C2530", border: "none" }} />
            <Line type="monotone" dataKey="risk" stroke="#378ADD" strokeWidth={2} dot={false} />
          </LineChart>
        </ResponsiveContainer>
      </div>

      <div style={{ background: "#141A22", borderRadius: "12px", padding: "20px" }}>
        <h3 style={{ marginBottom: "16px", color: "#A8B5C2" }}>Live Transactions</h3>
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr style={{ textAlign: "left", color: "#7C8B9C", fontSize: "13px" }}>
              <th style={{ padding: "8px" }}>ID</th>
              <th style={{ padding: "8px" }}>Amount</th>
              <th style={{ padding: "8px" }}>Risk Score</th>
              <th style={{ padding: "8px" }}>Status</th>
            </tr>
          </thead>
          <tbody>
            {transactions.map(t => (
              <tr key={t.id} style={{ borderTop: "1px solid #222A33" }}>
                <td style={{ padding: "8px", fontFamily: "monospace", fontSize: "13px" }}>{t.id.slice(0, 8)}</td>
                <td style={{ padding: "8px" }}>${t.amount.toFixed(2)}</td>
                <td style={{ padding: "8px" }}>{t.risk_score}%</td>
                <td style={{ padding: "8px" }}>
                  <span style={{
                    padding: "4px 10px",
                    borderRadius: "20px",
                    fontSize: "12px",
                    background: t.is_fraud ? "#E24B4A33" : "#34C77B33",
                    color: t.is_fraud ? "#E24B4A" : "#34C77B"
                  }}>
                    {t.is_fraud ? "FRAUD" : "OK"}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function StatCard({ label, value, color }) {
  return (
    <div style={{ background: "#141A22", borderRadius: "12px", padding: "20px" }}>
      <p style={{ color: "#7C8B9C", fontSize: "13px", marginBottom: "8px" }}>{label}</p>
      <p style={{ fontSize: "28px", fontWeight: 700, color }}>{value}</p>
    </div>
  );
}
