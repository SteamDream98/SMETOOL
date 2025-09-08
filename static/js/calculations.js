// Enhanced Real-time Calculations with Chart.js Integration

// Chart instances storage
const chartInstances = {};

// Real-time calculation functions
function initializeRealTimeCalculations() {
    // Debt Brake Calculator
    const debtBrakeInputs = document.querySelectorAll('#revenue, #expenses, #existingDebt, #debtServiceRatio');
    debtBrakeInputs.forEach(input => {
        if (input) {
            input.addEventListener('input', debounce(calculateDebtBrake, 500));
        }
    });
    
    // Cost Analysis Calculator
    const costAnalysisInputs = document.querySelectorAll('#principal, #interestRate, #term, #fees, #monthlyFees, #opportunityCost');
    costAnalysisInputs.forEach(input => {
        if (input) {
            input.addEventListener('input', debounce(calculateCostAnalysis, 500));
        }
    });
    
    // Debt Snowball Calculator
    const snowballInputs = document.querySelectorAll('#monthlyPayment');
    snowballInputs.forEach(input => {
        if (input) {
            input.addEventListener('input', debounce(calculateDebtSnowball, 500));
        }
    });
    
    // Load saved calculations on page load
    loadSavedCalculations();
}

// Debounce function for performance
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Enhanced calculation functions with real-time updates and charts
function calculateDebtBrake() {
    const revenue = parseFloat(document.getElementById('revenue')?.value) || 0;
    const expenses = parseFloat(document.getElementById('expenses')?.value) || 0;
    const existingDebt = parseFloat(document.getElementById('existingDebt')?.value) || 0;
    const debtServiceRatio = parseFloat(document.getElementById('debtServiceRatio')?.value) || 0.30;
    
    if (revenue > 0) {
        const netIncome = revenue - expenses;
        const maxDebtService = netIncome * debtServiceRatio;
        const debtLimit = revenue * 0.0035; // 0.35% of revenue
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
        
        // Update results in real-time
        updateDebtBrakeResults(results);
        
        // Create charts
        createDebtBrakeCharts(results);
        
        // Save calculation
        saveCalculation('debtBrake', results);
    }
}

function calculateCostAnalysis() {
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
        
        // Update results in real-time
        updateCostAnalysisResults(results);
        
        // Create charts
        createCostAnalysisCharts(results);
        
        // Save calculation
        saveCalculation('costAnalysis', results);
    }
}

function calculateDebtSnowball() {
    const monthlyPayment = parseFloat(document.getElementById('monthlyPayment')?.value) || 0;
    const debtEntries = document.querySelectorAll('.debt-entry');
    
    if (monthlyPayment > 0 && debtEntries.length > 0) {
        const debts = [];
        debtEntries.forEach(entry => {
            const name = entry.querySelector('.debt-name')?.value || '';
            const balance = parseFloat(entry.querySelector('.debt-balance')?.value) || 0;
            const rate = parseFloat(entry.querySelector('.debt-rate')?.value) || 0;
            
            if (name && balance > 0 && rate >= 0) {
                debts.push({ name, balance, rate });
            }
        });
        
        if (debts.length > 0) {
            // Sort by interest rate (highest first for snowball method)
            debts.sort((a, b) => b.rate - a.rate);
            
            let totalInterest = 0;
            let totalPaid = 0;
            let months = 0;
            
            debts.forEach(debt => {
                const monthlyRate = debt.rate / 100 / 12;
                const numPayments = Math.log(1 + (debt.balance * monthlyRate) / monthlyPayment) / Math.log(1 + monthlyRate);
                const interest = (monthlyPayment * numPayments) - debt.balance;
                totalInterest += interest;
                totalPaid += debt.balance + interest;
                months += numPayments;
            });
            
            const results = {
                totalInterest: totalInterest,
                totalPaid: totalPaid,
                totalMonths: months,
                monthlyPayment: monthlyPayment,
                debts: debts
            };
            
            // Update results in real-time
            updateDebtSnowballResults(results);
            
            // Create charts
            createDebtSnowballCharts(results);
            
            // Save calculation
            saveCalculation('debtSnowball', results);
        }
    }
}

// Chart creation functions
function createDebtBrakeCharts(results) {
    // Debt Usage Chart
    const debtUsageCtx = document.getElementById('debtUsageChart');
    if (debtUsageCtx) {
        if (chartInstances.debtUsage) {
            chartInstances.debtUsage.destroy();
        }
        
        chartInstances.debtUsage = new Chart(debtUsageCtx, {
            type: 'doughnut',
            data: {
                labels: ['Used Debt', 'Available Capacity'],
                datasets: [{
                    data: [results.existingDebt, results.availableCapacity],
                    backgroundColor: [
                        results.debtUsage > 80 ? '#dc3545' : results.debtUsage > 60 ? '#ffc107' : '#28a745',
                        '#e9ecef'
                    ],
                    borderWidth: 2,
                    borderColor: '#fff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom'
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return context.label + ': ' + formatCurrency(context.parsed);
                            }
                        }
                    }
                }
            }
        });
    }
    
    // Income vs Expenses Chart
    const incomeExpensesCtx = document.getElementById('incomeExpensesChart');
    if (incomeExpensesCtx) {
        if (chartInstances.incomeExpenses) {
            chartInstances.incomeExpenses.destroy();
        }
        
        chartInstances.incomeExpenses = new Chart(incomeExpensesCtx, {
            type: 'bar',
            data: {
                labels: ['Revenue', 'Expenses', 'Net Income'],
                datasets: [{
                    label: 'Amount (€)',
                    data: [results.revenue, results.expenses, results.netIncome],
                    backgroundColor: ['#28a745', '#dc3545', '#007bff'],
                    borderWidth: 1,
                    borderColor: '#fff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return formatCurrency(value);
                            }
                        }
                    }
                },
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return context.label + ': ' + formatCurrency(context.parsed.y);
                            }
                        }
                    }
                }
            }
        });
    }
}

function createCostAnalysisCharts(results) {
    // Cost Breakdown Chart
    const costBreakdownCtx = document.getElementById('costBreakdownChart');
    if (costBreakdownCtx) {
        if (chartInstances.costBreakdown) {
            chartInstances.costBreakdown.destroy();
        }
        
        chartInstances.costBreakdown = new Chart(costBreakdownCtx, {
            type: 'pie',
            data: {
                labels: ['Interest', 'Fees', 'Principal'],
                datasets: [{
                    data: [results.totalInterest, results.totalFees, results.principal],
                    backgroundColor: ['#ffc107', '#17a2b8', '#28a745'],
                    borderWidth: 2,
                    borderColor: '#fff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom'
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return context.label + ': ' + formatCurrency(context.parsed);
                            }
                        }
                    }
                }
            }
        });
    }
    
    // Payment Timeline Chart
    const paymentTimelineCtx = document.getElementById('paymentTimelineChart');
    if (paymentTimelineCtx) {
        if (chartInstances.paymentTimeline) {
            chartInstances.paymentTimeline.destroy();
        }
        
        // Generate monthly data
        const monthlyData = [];
        const labels = [];
        let remainingBalance = results.principal;
        
        for (let month = 1; month <= results.term * 12; month++) {
            const interestPayment = remainingBalance * (results.interestRate / 100 / 12);
            const principalPayment = results.monthlyPayment - interestPayment;
            remainingBalance -= principalPayment;
            
            monthlyData.push({
                month: month,
                principal: principalPayment,
                interest: interestPayment,
                balance: Math.max(0, remainingBalance)
            });
            
            if (month % 12 === 0) {
                labels.push(`Year ${Math.ceil(month / 12)}`);
            }
        }
        
        chartInstances.paymentTimeline = new Chart(paymentTimelineCtx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Remaining Balance',
                    data: monthlyData.filter((_, index) => index % 12 === 11).map(d => d.balance),
                    borderColor: '#dc3545',
                    backgroundColor: 'rgba(220, 53, 69, 0.1)',
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return formatCurrency(value);
                            }
                        }
                    }
                },
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return 'Remaining Balance: ' + formatCurrency(context.parsed.y);
                            }
                        }
                    }
                }
            }
        });
    }
}

function createDebtSnowballCharts(results) {
    // Debt Distribution Chart
    const debtDistributionCtx = document.getElementById('debtDistributionChart');
    if (debtDistributionCtx) {
        if (chartInstances.debtDistribution) {
            chartInstances.debtDistribution.destroy();
        }
        
        const colors = ['#dc3545', '#fd7e14', '#ffc107', '#28a745', '#20c997', '#0dcaf0', '#6f42c1'];
        
        chartInstances.debtDistribution = new Chart(debtDistributionCtx, {
            type: 'doughnut',
            data: {
                labels: results.debts.map(debt => debt.name),
                datasets: [{
                    data: results.debts.map(debt => debt.balance),
                    backgroundColor: colors.slice(0, results.debts.length),
                    borderWidth: 2,
                    borderColor: '#fff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom'
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return context.label + ': ' + formatCurrency(context.parsed);
                            }
                        }
                    }
                }
            }
        });
    }
}

// Enhanced result update functions with charts
function updateDebtBrakeResults(results) {
    const resultsDiv = document.getElementById('results');
    const resultsContent = document.getElementById('resultsContent');
    
    if (resultsDiv && resultsContent) {
        resultsContent.innerHTML = `
            <div class="row g-3">
                <div class="col-12 col-md-6">
                    <div class="card bg-light">
                        <div class="card-body text-center">
                            <h5 class="card-title text-primary">${formatCurrency(results.debtLimit)}</h5>
                            <p class="card-text">Maximum Debt Limit</p>
                        </div>
                    </div>
                </div>
                <div class="col-12 col-md-6">
                    <div class="card bg-light">
                        <div class="card-body text-center">
                            <h5 class="card-title text-success">${formatCurrency(results.availableCapacity)}</h5>
                            <p class="card-text">Available Capacity</p>
                        </div>
                    </div>
                </div>
                <div class="col-12 col-md-6">
                    <div class="card bg-light">
                        <div class="card-body text-center">
                            <h5 class="card-title text-warning">${results.debtUsage.toFixed(1)}%</h5>
                            <p class="card-text">Current Debt Usage</p>
                        </div>
                    </div>
                </div>
                <div class="col-12 col-md-6">
                    <div class="card bg-light">
                        <div class="card-body text-center">
                            <h5 class="card-title text-info">${formatCurrency(results.maxDebtService)}</h5>
                            <p class="card-text">Max Monthly Payment</p>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Charts Section -->
            <div class="row g-3 mt-4">
                <div class="col-12 col-md-6">
                    <div class="card">
                        <div class="card-header">
                            <h6 class="mb-0"><i class="fas fa-chart-pie me-2"></i>Debt Usage</h6>
                        </div>
                        <div class="card-body">
                            <canvas id="debtUsageChart" height="200"></canvas>
                        </div>
                    </div>
                </div>
                <div class="col-12 col-md-6">
                    <div class="card">
                        <div class="card-header">
                            <h6 class="mb-0"><i class="fas fa-chart-bar me-2"></i>Income vs Expenses</h6>
                        </div>
                        <div class="card-body">
                            <canvas id="incomeExpensesChart" height="200"></canvas>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Calculation History -->
            <div class="row g-3 mt-4">
                <div class="col-12">
                    <div class="card">
                        <div class="card-header d-flex justify-content-between align-items-center">
                            <h6 class="mb-0"><i class="fas fa-history me-2"></i>Calculation History</h6>
                            <button class="btn btn-outline-secondary btn-sm" onclick="clearCalculationHistory('debtBrake')">
                                <i class="fas fa-trash me-1"></i>Clear History
                            </button>
                        </div>
                        <div class="card-body">
                            <div id="debtBrakeHistory"></div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        resultsDiv.style.display = 'block';
        
        // Load calculation history
        loadCalculationHistory('debtBrake');
    }
}

function updateCostAnalysisResults(results) {
    const resultsDiv = document.getElementById('results');
    const resultsContent = document.getElementById('resultsContent');
    
    if (resultsDiv && resultsContent) {
        resultsContent.innerHTML = `
            <div class="row g-3">
                <div class="col-12 col-md-6">
                    <div class="card bg-light">
                        <div class="card-body text-center">
                            <h5 class="card-title text-primary">${formatCurrency(results.monthlyPayment)}</h5>
                            <p class="card-text">Monthly Payment</p>
                        </div>
                    </div>
                </div>
                <div class="col-12 col-md-6">
                    <div class="card bg-light">
                        <div class="card-body text-center">
                            <h5 class="card-title text-danger">${formatCurrency(results.totalInterest)}</h5>
                            <p class="card-text">Total Interest</p>
                        </div>
                    </div>
                </div>
                <div class="col-12 col-md-6">
                    <div class="card bg-light">
                        <div class="card-body text-center">
                            <h5 class="card-title text-warning">${formatCurrency(results.totalFees)}</h5>
                            <p class="card-text">Total Fees</p>
                        </div>
                    </div>
                </div>
                <div class="col-12 col-md-6">
                    <div class="card bg-light">
                        <div class="card-body text-center">
                            <h5 class="card-title text-dark">${formatCurrency(results.totalCost)}</h5>
                            <p class="card-text">Total Cost</p>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Charts Section -->
            <div class="row g-3 mt-4">
                <div class="col-12 col-md-6">
                    <div class="card">
                        <div class="card-header">
                            <h6 class="mb-0"><i class="fas fa-chart-pie me-2"></i>Cost Breakdown</h6>
                        </div>
                        <div class="card-body">
                            <canvas id="costBreakdownChart" height="200"></canvas>
                        </div>
                    </div>
                </div>
                <div class="col-12 col-md-6">
                    <div class="card">
                        <div class="card-header">
                            <h6 class="mb-0"><i class="fas fa-chart-line me-2"></i>Payment Timeline</h6>
                        </div>
                        <div class="card-body">
                            <canvas id="paymentTimelineChart" height="200"></canvas>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Calculation History -->
            <div class="row g-3 mt-4">
                <div class="col-12">
                    <div class="card">
                        <div class="card-header d-flex justify-content-between align-items-center">
                            <h6 class="mb-0"><i class="fas fa-history me-2"></i>Calculation History</h6>
                            <button class="btn btn-outline-secondary btn-sm" onclick="clearCalculationHistory('costAnalysis')">
                                <i class="fas fa-trash me-1"></i>Clear History
                            </button>
                        </div>
                        <div class="card-body">
                            <div id="costAnalysisHistory"></div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        resultsDiv.style.display = 'block';
        
        // Load calculation history
        loadCalculationHistory('costAnalysis');
    }
}

function updateDebtSnowballResults(results) {
    const resultsDiv = document.getElementById('results');
    const resultsContent = document.getElementById('resultsContent');
    
    if (resultsDiv && resultsContent) {
        resultsContent.innerHTML = `
            <div class="row g-3">
                <div class="col-12 col-md-6">
                    <div class="card bg-light">
                        <div class="card-body text-center">
                            <h5 class="card-title text-danger">${formatCurrency(results.totalInterest)}</h5>
                            <p class="card-text">Total Interest</p>
                        </div>
                    </div>
                </div>
                <div class="col-12 col-md-6">
                    <div class="card bg-light">
                        <div class="card-body text-center">
                            <h5 class="card-title text-primary">${formatCurrency(results.totalPaid)}</h5>
                            <p class="card-text">Total Paid</p>
                        </div>
                    </div>
                </div>
                <div class="col-12 col-md-6">
                    <div class="card bg-light">
                        <div class="card-body text-center">
                            <h5 class="card-title text-info">${Math.ceil(results.totalMonths)}</h5>
                            <p class="card-text">Months to Pay Off</p>
                        </div>
                    </div>
                </div>
                <div class="col-12 col-md-6">
                    <div class="card bg-light">
                        <div class="card-body text-center">
                            <h5 class="card-title text-success">${formatCurrency(results.monthlyPayment)}</h5>
                            <p class="card-text">Monthly Payment</p>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Charts Section -->
            <div class="row g-3 mt-4">
                <div class="col-12">
                    <div class="card">
                        <div class="card-header">
                            <h6 class="mb-0"><i class="fas fa-chart-pie me-2"></i>Debt Distribution</h6>
                        </div>
                        <div class="card-body">
                            <canvas id="debtDistributionChart" height="200"></canvas>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Calculation History -->
            <div class="row g-3 mt-4">
                <div class="col-12">
                    <div class="card">
                        <div class="card-header d-flex justify-content-between align-items-center">
                            <h6 class="mb-0"><i class="fas fa-history me-2"></i>Calculation History</h6>
                            <button class="btn btn-outline-secondary btn-sm" onclick="clearCalculationHistory('debtSnowball')">
                                <i class="fas fa-trash me-1"></i>Clear History
                            </button>
                        </div>
                        <div class="card-body">
                            <div id="debtSnowballHistory"></div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        resultsDiv.style.display = 'block';
        
        // Load calculation history
        loadCalculationHistory('debtSnowball');
    }
}

// Data persistence functions
function saveCalculation(type, results) {
    const calculations = JSON.parse(localStorage.getItem('smeCalculations') || '{}');
    if (!calculations[type]) {
        calculations[type] = [];
    }
    
    const calculation = {
        id: Date.now(),
        timestamp: new Date().toISOString(),
        results: results,
        inputs: getCurrentInputs(type)
    };
    
    calculations[type].unshift(calculation);
    
    // Keep only last 10 calculations
    if (calculations[type].length > 10) {
        calculations[type] = calculations[type].slice(0, 10);
    }
    
    localStorage.setItem('smeCalculations', JSON.stringify(calculations));
}

function getCurrentInputs(type) {
    const inputs = {};
    
    if (type === 'debtBrake') {
        inputs.revenue = document.getElementById('revenue')?.value || '';
        inputs.expenses = document.getElementById('expenses')?.value || '';
        inputs.existingDebt = document.getElementById('existingDebt')?.value || '';
        inputs.debtServiceRatio = document.getElementById('debtServiceRatio')?.value || '';
    } else if (type === 'costAnalysis') {
        inputs.principal = document.getElementById('principal')?.value || '';
        inputs.interestRate = document.getElementById('interestRate')?.value || '';
        inputs.term = document.getElementById('term')?.value || '';
        inputs.fees = document.getElementById('fees')?.value || '';
        inputs.monthlyFees = document.getElementById('monthlyFees')?.value || '';
        inputs.opportunityCost = document.getElementById('opportunityCost')?.value || '';
    }
    
    return inputs;
}

function loadCalculationHistory(type) {
    const calculations = JSON.parse(localStorage.getItem('smeCalculations') || '{}');
    const history = calculations[type] || [];
    const historyDiv = document.getElementById(`${type}History`);
    
    if (historyDiv && history.length > 0) {
        historyDiv.innerHTML = history.map(calc => `
            <div class="card mb-2">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-start">
                        <div>
                            <h6 class="card-title mb-1">${new Date(calc.timestamp).toLocaleString('de-DE')}</h6>
                            <p class="card-text small text-muted mb-0">
                                ${type === 'debtBrake' ? `Revenue: ${formatCurrency(calc.results.revenue)}` : 
                                  type === 'costAnalysis' ? `Principal: ${formatCurrency(calc.results.principal)}` : 
                                  `Monthly Payment: ${formatCurrency(calc.results.monthlyPayment)}`}
                            </p>
                        </div>
                        <div class="btn-group btn-group-sm">
                            <button class="btn btn-outline-primary" onclick="loadCalculation('${type}', ${calc.id})">
                                <i class="fas fa-undo me-1"></i>Load
                            </button>
                            <button class="btn btn-outline-danger" onclick="deleteCalculation('${type}', ${calc.id})">
                                <i class="fas fa-trash me-1"></i>Delete
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `).join('');
    } else if (historyDiv) {
        historyDiv.innerHTML = '<p class="text-muted text-center">No calculation history available.</p>';
    }
}

function loadCalculation(type, id) {
    const calculations = JSON.parse(localStorage.getItem('smeCalculations') || '{}');
    const calculation = calculations[type]?.find(calc => calc.id === id);
    
    if (calculation) {
        // Load inputs
        Object.entries(calculation.inputs).forEach(([key, value]) => {
            const input = document.getElementById(key);
            if (input) {
                input.value = value;
            }
        });
        
        // Trigger calculation
        if (type === 'debtBrake') {
            calculateDebtBrake();
        } else if (type === 'costAnalysis') {
            calculateCostAnalysis();
        } else if (type === 'debtSnowball') {
            calculateDebtSnowball();
        }
        
        showMobileSuccess('Calculation loaded successfully!');
    }
}

function deleteCalculation(type, id) {
    const calculations = JSON.parse(localStorage.getItem('smeCalculations') || '{}');
    if (calculations[type]) {
        calculations[type] = calculations[type].filter(calc => calc.id !== id);
        localStorage.setItem('smeCalculations', JSON.stringify(calculations));
        loadCalculationHistory(type);
        showMobileSuccess('Calculation deleted successfully!');
    }
}

function clearCalculationHistory(type) {
    const calculations = JSON.parse(localStorage.getItem('smeCalculations') || '{}');
    calculations[type] = [];
    localStorage.setItem('smeCalculations', JSON.stringify(calculations));
    loadCalculationHistory(type);
    showMobileSuccess('Calculation history cleared!');
}

function loadSavedCalculations() {
    // This function can be used to load saved calculations on page load
    // For now, we'll just ensure the history is displayed
    const currentPage = window.location.pathname;
    if (currentPage.includes('debt-brake')) {
        loadCalculationHistory('debtBrake');
    } else if (currentPage.includes('cost-analysis')) {
        loadCalculationHistory('costAnalysis');
    } else if (currentPage.includes('debt-snowball')) {
        loadCalculationHistory('debtSnowball');
    }
}

// Utility function for currency formatting
function formatCurrency(amount) {
    return new Intl.NumberFormat('de-DE', {
        style: 'currency',
        currency: 'EUR'
    }).format(amount);
}

// Export functionality
function exportToPDF() {
    const resultsContent = document.getElementById('resultsContent');
    if (resultsContent) {
        // Create a new window with the results
        const printWindow = window.open('', '_blank');
        printWindow.document.write(`
            <html>
                <head>
                    <title>SME Debt Management Tool - Results</title>
                    <style>
                        body { font-family: Arial, sans-serif; margin: 20px; }
                        .card { border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 5px; }
                        .text-primary { color: #007bff; }
                        .text-success { color: #28a745; }
                        .text-danger { color: #dc3545; }
                        .text-warning { color: #ffc107; }
                        .text-info { color: #17a2b8; }
                        .text-dark { color: #343a40; }
                        .row { display: flex; flex-wrap: wrap; }
                        .col-12 { width: 100%; }
                        .col-md-6 { width: 50%; }
                        @media (max-width: 768px) { .col-md-6 { width: 100%; } }
                    </style>
                </head>
                <body>
                    <h1>SME Debt Management Tool - Results</h1>
                    <p>Generated on: ${new Date().toLocaleDateString('de-DE')}</p>
                    ${resultsContent.innerHTML.replace(/<canvas[^>]*><\/canvas>/g, '<p class="text-muted">Chart data available in web version</p>')}
                </body>
            </html>
        `);
        printWindow.document.close();
        printWindow.print();
    }
}

function exportToExcel() {
    const resultsContent = document.getElementById('resultsContent');
    if (resultsContent) {
        // Create CSV data
        const cards = resultsContent.querySelectorAll('.card .card-body');
        let csvData = 'Metric,Value\n';
        
        cards.forEach(card => {
            const title = card.querySelector('.card-title')?.textContent || '';
            const text = card.querySelector('.card-text')?.textContent || '';
            if (title && text && !title.includes('Chart')) {
                csvData += `"${text}","${title}"\n`;
            }
        });
        
        // Download CSV
        const blob = new Blob([csvData], { type: 'text/csv' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'sme-debt-results.csv';
        a.click();
        window.URL.revokeObjectURL(url);
    }
}

// Initialize real-time calculations when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeRealTimeCalculations();
});

// Global functions for backward compatibility
window.calculateDebtBrake = calculateDebtBrake;
window.calculateCostAnalysis = calculateCostAnalysis;
window.calculateDebtSnowball = calculateDebtSnowball;
window.exportToPDF = exportToPDF;
window.exportToExcel = exportToExcel;
window.loadCalculation = loadCalculation;
window.deleteCalculation = deleteCalculation;
window.clearCalculationHistory = clearCalculationHistory;