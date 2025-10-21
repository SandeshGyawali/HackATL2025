"use client";

import { useState, useEffect } from "react";

interface Product {
  _id: string;
  name: string;
  description: string;
}

interface ProductionStep {
  _id: string;
  name: string;
  description: string;
  estimated_hours: number;
  total_cost: number;
  materials: Array<{
    _id: string;
    name: string;
    quantity: number;
    unit_price?: number;
  }>;
}

export default function Dashboard() {
  const [activeSection, setActiveSection] = useState("products");
  const [products, setProducts] = useState<Product[]>([]);
  const [selectedProduct, setSelectedProduct] = useState("");
  const [breakdownData, setBreakdownData] = useState<ProductionStep[]>([]);
  const [timeEstimate, setTimeEstimate] = useState<number | null>(null);
  const [costEstimate, setCostEstimate] = useState<number | null>(null);
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState<Array<{id: number, text: string, sender: 'user' | 'bot'}>>([]);
  const [inputMessage, setInputMessage] = useState("");
  const [simulationProduct, setSimulationProduct] = useState("");
  const [simulationDate, setSimulationDate] = useState("");
  const [simulationCity, setSimulationCity] = useState("");
  const [simulationResult, setSimulationResult] = useState<any>(null);

  const API_BASE = "http://localhost:8000";

  useEffect(() => {
    loadProducts();
  }, []);

  const loadProducts = async () => {
    try {
      const response = await fetch(`${API_BASE}/product`);
      const data = await response.json();
      setProducts(data);
    } catch (error) {
      console.error("Error loading products:", error);
    }
  };

  const loadBreakdown = async (productId: string) => {
    if (!productId) return;
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE}/production-step/${productId}`);
      const data = await response.json();
      setBreakdownData(data);
    } catch (error) {
      console.error("Error loading breakdown:", error);
    }
    setLoading(false);
  };

  const loadTimeEstimate = async (productId: string) => {
    if (!productId) return;
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE}/estimate/time/${productId}`);
      const data = await response.json();
      setTimeEstimate(data.total_estimated_hours);
    } catch (error) {
      console.error("Error loading time estimate:", error);
    }
    setLoading(false);
  };

  const loadCostEstimate = async (productId: string) => {
    if (!productId) return;
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE}/estimate/cost/${productId}`);
      const data = await response.json();
      setCostEstimate(data.total_estimated_cost);
    } catch (error) {
      console.error("Error loading cost estimate:", error);
    }
    setLoading(false);
  };

  const handleProductChange = (productId: string, section: string) => {
    setSelectedProduct(productId);
    if (section === "breakdown") loadBreakdown(productId);
    if (section === "time") loadTimeEstimate(productId);
    if (section === "cost") loadCostEstimate(productId);
  };

  const runSimulation = async () => {
    if (!simulationProduct || !simulationDate) return;
    
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE}/simulate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          product_id: simulationProduct,
          start_date: simulationDate,
          city: simulationCity
        }),
      });
      
      const data = await response.json();
      setSimulationResult(data);
    } catch (error) {
      console.error('Simulation error:', error);
    }
    setLoading(false);
  };

  const handleSendMessage = async () => {
    if (!inputMessage.trim()) return;
    
    const newMessage = {
      id: Date.now(),
      text: inputMessage,
      sender: 'user' as const
    };
    
    setMessages(prev => [...prev, newMessage]);
    const currentMessage = inputMessage;
    setInputMessage("");
    
    try {
      const response = await fetch(`${API_BASE}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: currentMessage }),
      });
      
      const data = await response.json();
      
      const botResponse = {
        id: Date.now() + 1,
        text: data.response || "I'm having trouble processing your request.",
        sender: 'bot' as const
      };
      
      setMessages(prev => [...prev, botResponse]);
    } catch (error) {
      const errorResponse = {
        id: Date.now() + 1,
        text: "Sorry, I'm having connection issues. Please try again.",
        sender: 'bot' as const
      };
      setMessages(prev => [...prev, errorResponse]);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-600 via-red-600 to-blue-800 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center text-white mb-10">
          <h1 className="text-4xl font-light mb-2">NASA Manufacturing Intelligent Dashboard</h1>
          <p className="text-blue-100">Manage your manufacturing processes</p>
        </div>

        {/* Dashboard Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8 h-[80vh]">
          {/* Sidebar */}
          <div className="lg:col-span-1">
            <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-6 border border-white/20 h-full">
              {/* Navigation */}
              <nav className="space-y-4">
                {[
                  { id: "products", label: "Products" },
                  { id: "breakdown", label: "Production Breakdown" },
                  { id: "estimation", label: "Estimation Tool" },
                  { id: "simulation", label: "Run Simulation" },
                  { id: "chat", label: "Chat Assistant" },
                ].map((item) => (
                  <button
                    key={item.id}
                    onClick={() => setActiveSection(item.id)}
                    className={`w-full text-left p-4 rounded-xl transition-all duration-300 ${
                      activeSection === item.id
                        ? "bg-white/20 text-white transform translate-x-1"
                        : "bg-white/10 text-white/80 hover:bg-white/15 hover:transform hover:translate-x-1"
                    }`}
                  >
                    {item.label}
                  </button>
                ))}
              </nav>
              

            </div>
          </div>

          {/* Content */}
          <div className="lg:col-span-3">
            <div className="bg-white/95 backdrop-blur-lg rounded-2xl p-8 h-full overflow-y-auto">
              {/* Products Section */}
              {activeSection === "products" && (
                <div>
                  <h2 className="text-2xl font-semibold text-gray-800 mb-6">Available Products</h2>
                  <div className="grid gap-4">
                    {products.map((product) => (
                      <div key={product._id} className="bg-white rounded-xl p-6 shadow-lg border border-gray-100">
                        <h3 className="text-xl font-semibold text-gray-800 mb-2">{product.name}</h3>
                        <p className="text-gray-600">{product.description}</p>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Production Breakdown Section */}
              {activeSection === "breakdown" && (
                <div>
                  <h2 className="text-2xl font-semibold text-gray-800 mb-6">Production Breakdown</h2>
                  <div className="mb-6">
                    <select
                      value={selectedProduct}
                      onChange={(e) => handleProductChange(e.target.value, "breakdown")}
                      className="p-3 border border-gray-300 rounded-lg text-gray-700 bg-white min-w-[200px]"
                    >
                      <option value="">Select a product</option>
                      {products.map((product) => (
                        <option key={product._id} value={product._id}>
                          {product.name}
                        </option>
                      ))}
                    </select>
                  </div>
                  {loading ? (
                    <div className="text-center text-gray-500 italic">Loading breakdown...</div>
                  ) : (
                    <div className="space-y-4">
                      {breakdownData.map((step) => (
                        <div key={step._id} className="bg-white rounded-xl p-6 shadow-lg border-l-4 border-blue-500">
                          <h3 className="text-lg font-semibold text-gray-800 mb-2">{step.name}</h3>
                          <p className="text-gray-600 mb-3">{step.description}</p>
                          <div className="grid grid-cols-2 gap-4 mb-4">
                            <div>
                              <span className="font-medium text-gray-700">Estimated Hours:</span>
                              <span className="ml-2 text-blue-600 font-semibold">{step.estimated_hours}</span>
                            </div>
                            <div>
                              <span className="font-medium text-gray-700">Step Cost:</span>
                              <span className="ml-2 text-green-600 font-semibold">${step.total_cost.toFixed(2)}</span>
                            </div>
                          </div>
                          <div>
                            <h4 className="font-medium text-gray-700 mb-2">Materials:</h4>
                            <div className="pl-4 space-y-1">
                              {step.materials.map((material) => (
                                <div key={material._id} className="text-sm text-gray-600">
                                  • {material.name} (Qty: {material.quantity}, Unit Price: ${material.unit_price || 0})
                                </div>
                              ))}
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )}

              {/* Estimation Tool Section */}
              {activeSection === "estimation" && (
                <div>
                  <h2 className="text-2xl font-semibold text-gray-800 mb-6">Estimation Tool</h2>
                  <div className="mb-6">
                    <select
                      value={selectedProduct}
                      onChange={(e) => {
                        setSelectedProduct(e.target.value);
                        if (e.target.value) {
                          loadTimeEstimate(e.target.value);
                          loadCostEstimate(e.target.value);
                        }
                      }}
                      className="p-3 border border-gray-300 rounded-lg text-gray-700 bg-white min-w-[200px]"
                    >
                      <option value="">Select a product</option>
                      {products.map((product) => (
                        <option key={product._id} value={product._id}>
                          {product.name}
                        </option>
                      ))}
                    </select>
                  </div>
                  {loading ? (
                    <div className="text-center text-gray-500 italic">Loading estimates...</div>
                  ) : (
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      {timeEstimate !== null && (
                        <div className="bg-white rounded-xl p-8 shadow-lg text-center">
                          <h3 className="text-xl font-semibold text-gray-800 mb-4">Production Time</h3>
                          <div className="text-4xl font-bold text-blue-600 mb-4">{timeEstimate} hours</div>
                          <p className="text-gray-600">Estimated time to complete production</p>
                        </div>
                      )}
                      {costEstimate !== null && (
                        <div className="bg-white rounded-xl p-8 shadow-lg text-center">
                          <h3 className="text-xl font-semibold text-gray-800 mb-4">Production Cost</h3>
                          <div className="text-4xl font-bold text-green-600 mb-4">${costEstimate.toFixed(2)}</div>
                          <p className="text-gray-600">Estimated cost for materials and production</p>
                        </div>
                      )}
                    </div>
                  )}
                </div>
              )}

              {/* Simulation Section */}
              {activeSection === "simulation" && (
                <div>
                  <h2 className="text-2xl font-semibold text-gray-800 mb-6">Production Simulation</h2>
                  <div className="bg-white rounded-xl p-6 shadow-lg mb-6">
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">Select Product</label>
                        <select
                          value={simulationProduct}
                          onChange={(e) => setSimulationProduct(e.target.value)}
                          className="w-full p-3 border border-gray-300 rounded-lg text-gray-700 bg-white"
                        >
                          <option value="">Choose a product</option>
                          {products.map((product) => (
                            <option key={product._id} value={product._id}>
                              {product.name}
                            </option>
                          ))}
                        </select>
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">Start Date</label>
                        <input
                          type="date"
                          value={simulationDate}
                          onChange={(e) => setSimulationDate(e.target.value)}
                          className="w-full p-3 border border-gray-300 rounded-lg text-gray-700 bg-white"
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">City</label>
                        <select
                          value={simulationCity}
                          onChange={(e) => setSimulationCity(e.target.value)}
                          className="w-full p-3 border border-gray-300 rounded-lg text-gray-700 bg-white"
                        >
                          <option value="">Select city</option>
                          <option value="New York">New York</option>
                          <option value="Los Angeles">Los Angeles</option>
                          <option value="Chicago">Chicago</option>
                          <option value="Miami">Miami</option>
                          <option value="Seattle">Seattle</option>
                          <option value="Houston">Houston</option>
                          <option value="Phoenix">Phoenix</option>
                          <option value="Boston">Boston</option>
                          <option value="Michigan">Michigan</option>
                        </select>
                      </div>
                    </div>
                    <button
                      onClick={runSimulation}
                      disabled={!simulationProduct || !simulationDate || !simulationCity || loading}
                      className="w-full bg-blue-600 text-white py-3 px-6 rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
                    >
                      {loading ? "Running Simulation..." : "Run Simulation"}
                    </button>
                  </div>
                  
                  {simulationResult && (
                    <div className="bg-white rounded-xl p-6 shadow-lg">
                      <h3 className="text-xl font-semibold text-gray-800 mb-4">Simulation Results</h3>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                        <div className="bg-blue-50 p-4 rounded-lg">
                          <h4 className="font-semibold text-blue-800">Production Timeline</h4>
                          <p className="text-sm text-gray-600">Start: {simulationResult.start_date}</p>
                          <p className="text-sm text-gray-600">Completion: {simulationResult.completion_date}</p>
                          <p className="text-sm text-gray-600">Duration: {simulationResult.work_days} work days</p>
                        </div>
                        <div className="bg-blue-50 p-4 rounded-lg">
                          <h4 className="font-semibold text-blue-800">Weather Forecast</h4>
                          <p className="text-sm text-gray-600">Condition: {simulationResult.weather?.condition}</p>
                        </div>
                      </div>
                      <div
                        className={`p-4 rounded-lg ${
                          simulationResult.delivery_recommendation === 0
                            ? "bg-green-100"
                            : simulationResult.delivery_recommendation === 2
                            ? "bg-red-100"
                            : "bg-yellow-50"
                        }`}
                      >
                        <h4
                          className={`font-semibold ${
                            simulationResult.delivery_recommendation === 0
                              ? "text-green-800"
                              : simulationResult.delivery_recommendation === 2
                              ? "text-red-800"
                              : "text-yellow-800"
                          }`}
                        >
                          Recommendation
                        </h4>
                        <p className="text-gray-700">{simulationResult.recommendation}</p>
                      </div>

                    </div>
                  )}
                </div>
              )}

              {/* Chat Section */}
              {activeSection === "chat" && (
                <div>
                  <h2 className="text-2xl font-semibold text-gray-800 mb-6">Chat Assistant</h2>
                  <div className="bg-white rounded-xl p-6 shadow-lg h-96 flex flex-col">
                    {/* Messages */}
                    <div className="flex-1 overflow-y-auto mb-4 p-4 bg-gray-50 rounded-lg">
                      {messages.length === 0 ? (
                        <p className="text-gray-500 text-center">Start a conversation with the AI assistant...</p>
                      ) : (
                        <div className="space-y-3">
                          {messages.map((message) => (
                            <div
                              key={message.id}
                              className={`flex ${
                                message.sender === 'user' ? 'justify-end' : 'justify-start'
                              }`}
                            >
                              <div
                                className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                                  message.sender === 'user'
                                    ? 'bg-blue-500 text-white'
                                    : 'bg-gray-200 text-gray-800'
                                }`}
                              >
                                {message.text}
                              </div>
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                    
                    {/* Input */}
                    <div className="flex gap-3">
                      <input
                        type="text"
                        value={inputMessage}
                        onChange={(e) => setInputMessage(e.target.value)}
                        onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                        placeholder="Ask about NASA products, production steps, costs, or time estimates..."
                        className="flex-1 p-3 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500 text-gray-900 bg-white"
                      />
                      <button
                        onClick={handleSendMessage}
                        disabled={!inputMessage.trim()}
                        className="px-6 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
                      >
                        Send
                      </button>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
