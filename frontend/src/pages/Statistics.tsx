import { ArrowLeft, TrendingUp, Calendar, Zap } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from "recharts";

const Statistics = () => {
    const navigate = useNavigate();

    const weeklyData = [
        { day: "Mon", calories: 2100 },
        { day: "Tue", calories: 1800 },
        { day: "Wed", calories: 2400 },
        { day: "Thu", calories: 1950 },
        { day: "Fri", calories: 2300 },
        { day: "Sat", calories: 2600 },
        { day: "Sun", calories: 2000 },
    ];

    const macroData = [
        { name: "Protein", value: 140, color: "#10b981", percent: 85 },
        { name: "Carbs", value: 220, color: "#3b82f6", percent: 65 },
        { name: "Fats", value: 65, color: "#f59e0b", percent: 45 },
    ];

    return (
        <div className="min-h-screen bg-background flex flex-col">
            {/* Header */}
            <header className="flex items-center gap-4 px-6 py-4 border-b border-border/50 backdrop-blur-md sticky top-0 z-50 bg-background/80">
                <button
                    onClick={() => navigate("/capture")}
                    className="w-10 h-10 rounded-full bg-secondary flex items-center justify-center hover:bg-secondary/80 transition-colors"
                >
                    <ArrowLeft size={20} className="text-foreground" />
                </button>
                <h1 className="text-xl font-semibold text-foreground">Statistics</h1>
            </header>

            <main className="flex-1 p-6 scrollbar-hide">
                <div className="max-w-md mx-auto space-y-6">

                    {/* Weekly Chart */}
                    <div className="glass-card rounded-3xl p-6 animate-slide-up">
                        <div className="flex items-center justify-between mb-6">
                            <h2 className="font-semibold text-foreground flex items-center gap-2">
                                <Calendar size={18} className="text-primary" />
                                Weekly Intake
                            </h2>
                            <span className="text-xs text-muted-foreground">Last 7 Days</span>
                        </div>

                        <div className="h-[200px] w-full">
                            <ResponsiveContainer width="100%" height="100%">
                                <BarChart data={weeklyData}>
                                    <XAxis
                                        dataKey="day"
                                        axisLine={false}
                                        tickLine={false}
                                        tick={{ fill: '#888', fontSize: 12 }}
                                        dy={10}
                                    />
                                    <Tooltip
                                        cursor={{ fill: 'rgba(255,255,255,0.05)' }}
                                        contentStyle={{ backgroundColor: '#1a1a1a', border: 'none', borderRadius: '8px', boxShadow: '0 4px 12px rgba(0,0,0,0.5)' }}
                                        itemStyle={{ color: '#fff' }}
                                    />
                                    <Bar dataKey="calories" radius={[4, 4, 0, 0]}>
                                        {weeklyData.map((entry, index) => (
                                            <Cell key={`cell-${index}`} fill={entry.calories > 2200 ? '#f59e0b' : '#3b82f6'} />
                                        ))}
                                    </Bar>
                                </BarChart>
                            </ResponsiveContainer>
                        </div>
                    </div>

                    {/* Macro Progress */}
                    <div className="glass-card rounded-3xl p-6 animate-slide-up" style={{ animationDelay: '0.1s' }}>
                        <div className="flex items-center justify-between mb-6">
                            <h2 className="font-semibold text-foreground flex items-center gap-2">
                                <Zap size={18} className="text-yellow-400" />
                                Macro Goals
                            </h2>
                            <span className="text-xs text-muted-foreground">Daily Average</span>
                        </div>

                        <div className="space-y-6">
                            {macroData.map((item) => (
                                <div key={item.name}>
                                    <div className="flex justify-between text-sm mb-2">
                                        <span className="text-muted-foreground">{item.name}</span>
                                        <span className="font-medium text-foreground">{item.value}g</span>
                                    </div>
                                    <div className="h-3 w-full bg-secondary rounded-full overflow-hidden">
                                        <div
                                            className="h-full rounded-full transition-all duration-1000"
                                            style={{ width: `${item.percent}%`, backgroundColor: item.color }}
                                        />
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>

                    {/* Trend Card */}
                    <div className="bg-gradient-to-br from-primary/20 to-primary/5 rounded-3xl p-6 border border-primary/20 animate-slide-up" style={{ animationDelay: '0.2s' }}>
                        <div className="flex items-start gap-4">
                            <div className="w-12 h-12 rounded-full bg-primary/20 flex items-center justify-center shrink-0">
                                <TrendingUp size={24} className="text-primary" />
                            </div>
                            <div>
                                <h3 className="font-semibold text-foreground mb-1">On Track!</h3>
                                <p className="text-sm text-muted-foreground">
                                    You've met your calorie goal for 5 out of 7 days this week. Keep it up!
                                </p>
                            </div>
                        </div>
                    </div>

                </div>
            </main>
        </div>
    );
};

export default Statistics;
