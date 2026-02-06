import { ArrowLeft, Calendar, Clock, ChevronRight } from "lucide-react";
import { useNavigate } from "react-router-dom";

const History = () => {
    const navigate = useNavigate();

    const historyItems = [
        {
            id: 1,
            image: "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=600&q=80",
            name: "Green Salad Bowl",
            calories: 320,
            macros: "12g P • 24g C • 18g F",
            date: "Today",
            time: "12:30 PM"
        },
        {
            id: 2,
            image: "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=600&q=80",
            name: "Pepperoni Pizza Slice",
            calories: 285,
            macros: "11g P • 32g C • 14g F",
            date: "Today",
            time: "10:15 AM"
        },
        {
            id: 3,
            image: "https://images.unsplash.com/photo-1482049016688-2d3e1b311543?w=600&q=80",
            name: "Avocado Toast",
            calories: 450,
            macros: "12g P • 48g C • 22g F",
            date: "Yesterday",
            time: "9:00 AM"
        },
        {
            id: 4,
            image: "https://images.unsplash.com/photo-1467003909585-2f8a7270028d?w=600&q=80",
            name: "Salmon Dinner",
            calories: 650,
            macros: "45g P • 8g C • 32g F",
            date: "Yesterday",
            time: "7:30 PM"
        },
        {
            id: 5,
            image: "https://images.unsplash.com/photo-1484723091739-30a097e8f929?w=600&q=80",
            name: "French Toast",
            calories: 520,
            macros: "14g P • 62g C • 24g F",
            date: "Mon, Feb 2",
            time: "8:45 AM"
        }
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
                <h1 className="text-xl font-semibold text-foreground">Food History</h1>
            </header>

            <main className="flex-1 p-6">
                <div className="max-w-md mx-auto space-y-4">
                    {historyItems.map((item, index) => (
                        <div
                            key={item.id}
                            className="glass-card rounded-2xl p-3 flex items-center gap-4 hover:bg-white/5 transition-colors cursor-pointer animate-slide-up"
                            style={{ animationDelay: `${index * 0.05}s` }}
                        >
                            <div className="w-20 h-20 rounded-xl overflow-hidden shadow-md shrink-0">
                                <img src={item.image} alt={item.name} className="w-full h-full object-cover" />
                            </div>

                            <div className="flex-1 min-w-0">
                                <div className="flex items-center justify-between mb-1">
                                    <h3 className="font-semibold text-foreground truncate">{item.name}</h3>
                                    <span className="text-xs font-semibold text-primary bg-primary/10 px-2 py-0.5 rounded-full">
                                        {item.calories} cal
                                    </span>
                                </div>
                                <p className="text-xs text-muted-foreground mb-2">{item.macros}</p>
                                <div className="flex items-center gap-3 text-[10px] text-muted-foreground">
                                    <span className="flex items-center gap-1">
                                        <Calendar size={10} /> {item.date}
                                    </span>
                                    <span className="flex items-center gap-1">
                                        <Clock size={10} /> {item.time}
                                    </span>
                                </div>
                            </div>

                            <ChevronRight size={16} className="text-muted-foreground" />
                        </div>
                    ))}
                </div>
            </main>
        </div>
    );
};

export default History;
