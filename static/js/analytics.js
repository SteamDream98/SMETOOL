// Advanced Analytics and Insights for SME Debt Management Tool

class SMEAnalytics {
    constructor() {
        this.analyticsData = this.loadAnalyticsData();
        this.insights = [];
        this.recommendations = [];
    }

    // Load analytics data from localStorage
    loadAnalyticsData() {
        const data = JSON.parse(localStorage.getItem('smeAnalytics') || '{}');
        return {
            calculations: data.calculations || [],
            userBehavior: data.userBehavior || {},
            trends: data.trends || {},
            insights: data.insights || [],
            ...data
        };
    }

    // Save analytics data
    saveAnalyticsData() {
        localStorage.setItem('smeAnalytics', JSON.stringify(this.analyticsData));
    }

    // Track calculation
    trackCalculation(type, inputs, results) {
        const calculation = {
            id: Date.now(),
            timestamp: new Date().toISOString(),
            type: type,
            inputs: inputs,
            results: results,
            sessionId: this.getSessionId()
        };

        this.analyticsData.calculations.push(calculation);
        
        // Keep only last 100 calculations
        if (this.analyticsData.calculations.length > 100) {
            this.analyticsData.calculations = this.analyticsData.calculations.slice(-100);
        }

        this.generateInsights();
        this.saveAnalyticsData();
    }

    // Track user behavior
    trackUserBehavior(action, data = {}) {
        if (!this.analyticsData.userBehavior[action]) {
            this.analyticsData.userBehavior[action] = [];
        }

        this.analyticsData.userBehavior[action].push({
            timestamp: new Date().toISOString(),
            ...data
        });

        this.saveAnalyticsData();
    }

    // Generate insights based on calculation history
    generateInsights() {
        this.insights = [];
        const calculations = this.analyticsData.calculations;

        if (calculations.length < 2) return;

        // Debt trend analysis
        const debtCalculations = calculations.filter(c => c.type === 'debtBrake');
        if (debtCalculations.length >= 2) {
            this.analyzeDebtTrends(debtCalculations);
        }

        // Cost analysis trends
        const costCalculations = calculations.filter(c => c.type === 'costAnalysis');
        if (costCalculations.length >= 2) {
            this.analyzeCostTrends(costCalculations);
        }

        // Cross-analysis insights
        this.generateCrossAnalysisInsights();
    }

    // Analyze debt trends
    analyzeDebtTrends(calculations) {
        const recent = calculations.slice(-3);
        const older = calculations.slice(-6, -3);

        if (recent.length >= 2 && older.length >= 2) {
            const recentAvgDebt = recent.reduce((sum, c) => sum + c.results.existingDebt, 0) / recent.length;
            const olderAvgDebt = older.reduce((sum, c) => sum + c.results.existingDebt, 0) / older.length;

            const debtChange = ((recentAvgDebt - olderAvgDebt) / olderAvgDebt) * 100;

            if (Math.abs(debtChange) > 10) {
                this.insights.push({
                    type: 'debt_trend',
                    priority: debtChange > 0 ? 'high' : 'medium',
                    title: debtChange > 0 ? 'Debt Level Increasing' : 'Debt Level Decreasing',
                    message: `Your debt level has ${debtChange > 0 ? 'increased' : 'decreased'} by ${Math.abs(debtChange).toFixed(1)}% in recent calculations.`,
                    recommendation: debtChange > 0 ? 
                        'Consider reviewing your spending and increasing debt payments.' : 
                        'Great job! Continue your debt reduction strategy.',
                    icon: debtChange > 0 ? 'fas fa-arrow-up text-danger' : 'fas fa-arrow-down text-success'
                });
            }
        }
    }

    // Analyze cost trends
    analyzeCostTrends(calculations) {
        const recent = calculations.slice(-3);
        const older = calculations.slice(-6, -3);

        if (recent.length >= 2 && older.length >= 2) {
            const recentAvgRate = recent.reduce((sum, c) => sum + c.inputs.interestRate, 0) / recent.length;
            const olderAvgRate = older.reduce((sum, c) => sum + c.inputs.interestRate, 0) / older.length;

            const rateChange = recentAvgRate - olderAvgRate;

            if (Math.abs(rateChange) > 0.5) {
                this.insights.push({
                    type: 'interest_trend',
                    priority: rateChange > 0 ? 'high' : 'low',
                    title: rateChange > 0 ? 'Interest Rates Rising' : 'Interest Rates Falling',
                    message: `Average interest rates in your calculations have ${rateChange > 0 ? 'increased' : 'decreased'} by ${Math.abs(rateChange).toFixed(2)}%.`,
                    recommendation: rateChange > 0 ? 
                        'Consider locking in lower rates or refinancing existing debt.' : 
                        'Good time to consider new financing at lower rates.',
                    icon: rateChange > 0 ? 'fas fa-chart-line text-warning' : 'fas fa-chart-line text-success'
                });
            }
        }
    }

    // Generate cross-analysis insights
    generateCrossAnalysisInsights() {
        const debtCalculations = this.analyticsData.calculations.filter(c => c.type === 'debtBrake');
        const costCalculations = this.analyticsData.calculations.filter(c => c.type === 'costAnalysis');

        if (debtCalculations.length > 0 && costCalculations.length > 0) {
            const latestDebt = debtCalculations[debtCalculations.length - 1];
            const latestCost = costCalculations[costCalculations.length - 1];

            // Compare debt capacity with loan costs
            const debtCapacity = latestDebt.results.availableCapacity;
            const loanAmount = latestCost.inputs.principal;

            if (loanAmount > debtCapacity) {
                this.insights.push({
                    type: 'capacity_warning',
                    priority: 'high',
                    title: 'Loan Exceeds Debt Capacity',
                    message: `The loan amount (${formatCurrency(loanAmount)}) exceeds your available debt capacity (${formatCurrency(debtCapacity)}).`,
                    recommendation: 'Consider reducing the loan amount or improving your financial position first.',
                    icon: 'fas fa-exclamation-triangle text-danger'
                });
            }
        }
    }

    // Get session ID
    getSessionId() {
        let sessionId = sessionStorage.getItem('smeSessionId');
        if (!sessionId) {
            sessionId = 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
            sessionStorage.setItem('smeSessionId', sessionId);
        }
        return sessionId;
    }

    // Get insights for display
    getInsights() {
        return this.insights.sort((a, b) => {
            const priorityOrder = { high: 3, medium: 2, low: 1 };
            return priorityOrder[b.priority] - priorityOrder[a.priority];
        });
    }

    // Get analytics summary
    getAnalyticsSummary() {
        const calculations = this.analyticsData.calculations;
        const totalCalculations = calculations.length;
        const calculationTypes = {};
        
        calculations.forEach(calc => {
            calculationTypes[calc.type] = (calculationTypes[calc.type] || 0) + 1;
        });

        const mostUsedTool = Object.keys(calculationTypes).reduce((a, b) => 
            calculationTypes[a] > calculationTypes[b] ? a : b, 'debtBrake');

        return {
            totalCalculations,
            calculationTypes,
            mostUsedTool,
            insightsCount: this.insights.length,
            lastCalculation: calculations.length > 0 ? calculations[calculations.length - 1].timestamp : null
        };
    }

    // Generate recommendations
    generateRecommendations() {
        this.recommendations = [];
        const summary = this.getAnalyticsSummary();

        // Usage-based recommendations
        if (summary.totalCalculations < 3) {
            this.recommendations.push({
                type: 'usage',
                title: 'Explore All Tools',
                message: 'Try all available calculators to get a complete picture of your financial situation.',
                action: 'Explore tools',
                icon: 'fas fa-compass text-info'
            });
        }

        // Tool-specific recommendations
        if (summary.calculationTypes.debtBrake && summary.calculationTypes.costAnalysis) {
            this.recommendations.push({
                type: 'integration',
                title: 'Compare Debt vs. Costs',
                message: 'Use both debt brake and cost analysis tools together for comprehensive planning.',
                action: 'Compare results',
                icon: 'fas fa-balance-scale text-primary'
            });
        }

        // Trend-based recommendations
        const highPriorityInsights = this.insights.filter(i => i.priority === 'high');
        if (highPriorityInsights.length > 0) {
            this.recommendations.push({
                type: 'urgent',
                title: 'Address High Priority Issues',
                message: `You have ${highPriorityInsights.length} high-priority insights that need attention.`,
                action: 'Review insights',
                icon: 'fas fa-exclamation-circle text-danger'
            });
        }

        return this.recommendations;
    }

    // Export analytics data
    exportAnalytics() {
        const data = {
            summary: this.getAnalyticsSummary(),
            insights: this.insights,
            recommendations: this.recommendations,
            calculations: this.analyticsData.calculations,
            exportedAt: new Date().toISOString()
        };

        const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'sme-analytics-export.json';
        a.click();
        window.URL.revokeObjectURL(url);
    }

    // Clear analytics data
    clearAnalytics() {
        this.analyticsData = {
            calculations: [],
            userBehavior: {},
            trends: {},
            insights: []
        };
        this.insights = [];
        this.recommendations = [];
        this.saveAnalyticsData();
    }
}

// Global analytics instance
const smeAnalytics = new SMEAnalytics();

// Enhanced calculation functions with analytics
function calculateDebtBrakeWithAnalytics() {
    const revenue = parseFloat(document.getElementById('revenue')?.value) || 0;
    const expenses = parseFloat(document.getElementById('expenses')?.value) || 0;
    const existingDebt = parseFloat(document.getElementById('existingDebt')?.value) || 0;
    const debtServiceRatio = parseFloat(document.getElementById('debtServiceRatio')?.value) || 0.30;
    
    if (revenue > 0) {
        const netIncome = revenue - expenses;
        const maxDebtService = netIncome * debtServiceRatio;
        const debtLimit = revenue * 0.0035;
        const availableCapacity = Math.max(0, debtLimit - existingDebt);
        const debtUsage = existingDebt > 0 ? (existingDebt / debtLimit) * 100 : 0;
        
        const results = {
            debtLimit: debtLimit,
            availableCapacity: availableCapacity,
            debtUsage: debtUsage,
            maxDebtService: maxDebtService,
            netIncome: netIncome,
            revenue: revenue,
            expenses: expenses,
            existingDebt: existingDebt
        };
        
        const inputs = {
            revenue: revenue,
            expenses: expenses,
            existingDebt: existingDebt,
            debtServiceRatio: debtServiceRatio
        };
        
        // Track calculation
        smeAnalytics.trackCalculation('debtBrake', inputs, results);
        
        // Update results
        updateDebtBrakeResults(results);
        createDebtBrakeCharts(results);
        
        // Show insights
        showInsights();
    }
}

function calculateCostAnalysisWithAnalytics() {
    const principal = parseFloat(document.getElementById('principal')?.value) || 0;
    const interestRate = parseFloat(document.getElementById('interestRate')?.value) || 0;
    const term = parseFloat(document.getElementById('term')?.value) || 0;
    const fees = parseFloat(document.getElementById('fees')?.value) || 0;
    const monthlyFees = parseFloat(document.getElementById('monthlyFees')?.value) || 0;
    const opportunityCost = parseFloat(document.getElementById('opportunityCost')?.value) || 8;
    
    if (principal > 0 && interestRate > 0 && term > 0) {
        const monthlyRate = interestRate / 100 / 12;
        const numPayments = term * 12;
        const monthlyPayment = principal * (monthlyRate * Math.pow(1 + monthlyRate, numPayments)) / (Math.pow(1 + monthlyRate, numPayments) - 1);
        const totalPayment = monthlyPayment * numPayments;
        const totalInterest = totalPayment - principal;
        const totalFees = fees + (monthlyFees * numPayments);
        const totalCost = totalInterest + totalFees;
        
        const results = {
            principal: principal,
            monthlyPayment: monthlyPayment,
            totalPayment: totalPayment,
            totalInterest: totalInterest,
            totalFees: totalFees,
            totalCost: totalCost,
            opportunityCost: opportunityCost,
            interestRate: interestRate,
            term: term
        };
        
        const inputs = {
            principal: principal,
            interestRate: interestRate,
            term: term,
            fees: fees,
            monthlyFees: monthlyFees,
            opportunityCost: opportunityCost
        };
        
        // Track calculation
        smeAnalytics.trackCalculation('costAnalysis', inputs, results);
        
        // Update results
        updateCostAnalysisResults(results);
        createCostAnalysisCharts(results);
        
        // Show insights
        showInsights();
    }
}

// Show insights in UI
function showInsights() {
    const insights = smeAnalytics.getInsights();
    const recommendations = smeAnalytics.generateRecommendations();
    
    // Create insights section if it doesn't exist
    let insightsSection = document.getElementById('insightsSection');
    if (!insightsSection) {
        insightsSection = document.createElement('div');
        insightsSection.id = 'insightsSection';
        insightsSection.className = 'row g-3 mt-4';
        
        const resultsDiv = document.getElementById('results');
        if (resultsDiv) {
            resultsDiv.appendChild(insightsSection);
        }
    }
    
    if (insights.length > 0 || recommendations.length > 0) {
        insightsSection.innerHTML = `
            ${insights.length > 0 ? `
                <div class="col-12">
                    <div class="card">
                        <div class="card-header">
                            <h6 class="mb-0"><i class="fas fa-lightbulb me-2"></i>AI Insights</h6>
                        </div>
                        <div class="card-body">
                            ${insights.map(insight => `
                                <div class="alert alert-${insight.priority === 'high' ? 'danger' : insight.priority === 'medium' ? 'warning' : 'info'} mb-3">
                                    <div class="d-flex align-items-start">
                                        <i class="${insight.icon} me-3 mt-1"></i>
                                        <div>
                                            <h6 class="alert-heading mb-1">${insight.title}</h6>
                                            <p class="mb-2">${insight.message}</p>
                                            <small class="text-muted"><strong>Recommendation:</strong> ${insight.recommendation}</small>
                                        </div>
                                    </div>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                </div>
            ` : ''}
            
            ${recommendations.length > 0 ? `
                <div class="col-12">
                    <div class="card">
                        <div class="card-header">
                            <h6 class="mb-0"><i class="fas fa-star me-2"></i>Recommendations</h6>
                        </div>
                        <div class="card-body">
                            ${recommendations.map(rec => `
                                <div class="card mb-3">
                                    <div class="card-body">
                                        <div class="d-flex align-items-start">
                                            <i class="${rec.icon} me-3 mt-1"></i>
                                            <div class="flex-grow-1">
                                                <h6 class="card-title mb-1">${rec.title}</h6>
                                                <p class="card-text mb-2">${rec.message}</p>
                                                <button class="btn btn-outline-primary btn-sm">${rec.action}</button>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                </div>
            ` : ''}
        `;
    }
}

// Track user behavior
function trackUserBehavior(action, data = {}) {
    smeAnalytics.trackUserBehavior(action, data);
}

// Initialize analytics when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Track page view
    trackUserBehavior('page_view', {
        page: window.location.pathname,
        timestamp: new Date().toISOString()
    });
    
    // Track form interactions
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            trackUserBehavior('form_submit', {
                formId: form.id,
                page: window.location.pathname
            });
        });
    });
    
    // Track button clicks
    const buttons = document.querySelectorAll('button');
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            trackUserBehavior('button_click', {
                buttonText: button.textContent.trim(),
                buttonClass: button.className,
                page: window.location.pathname
            });
        });
    });
});

// Global functions
window.smeAnalytics = smeAnalytics;
window.calculateDebtBrakeWithAnalytics = calculateDebtBrakeWithAnalytics;
window.calculateCostAnalysisWithAnalytics = calculateCostAnalysisWithAnalytics;
window.trackUserBehavior = trackUserBehavior;
window.showInsights = showInsights;
