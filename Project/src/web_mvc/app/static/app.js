// OMS Frontend Logic
document.addEventListener("DOMContentLoaded", () => {
    // API Base URL
    const API_BASE = "/api";

    // Application state
    let currentUser = null;
    let token = localStorage.getItem("token");

    // UI Cache Elements
    const navItems = document.querySelectorAll(".nav-item");
    const tabPanes = document.querySelectorAll(".tab-pane");
    const pageTitle = document.getElementById("page-title");
    
    // Auth elements
    const authSection = document.getElementById("auth-section");
    const tabLoginBtn = document.getElementById("tab-login-btn");
    const tabRegisterBtn = document.getElementById("tab-register-btn");
    const formLogin = document.getElementById("form-login");
    const formRegister = document.getElementById("form-register");
    const authAlert = document.getElementById("auth-alert");
    
    // Sidebar elements
    const userDisplayName = document.getElementById("user-display-name");
    const userDisplayRole = document.getElementById("user-display-role");
    const btnLogout = document.getElementById("btn-logout");
    
    // Dashboard Stats elements
    const dbTotalUsers = document.getElementById("dashboard-total-users");
    const dbPendingOrders = document.getElementById("dashboard-pending-orders");
    const dbShippedOrders = document.getElementById("dashboard-shipped-orders");
    
    // Users table body
    const usersTableBody = document.querySelector("#users-table tbody");
    const userCountBadge = document.getElementById("user-count-badge");
    
    // Orders elements
    const formOrder = document.getElementById("form-order");
    const orderAlert = document.getElementById("order-alert");
    const ordersTableBody = document.querySelector("#orders-table tbody");
    const btnRefreshOrders = document.getElementById("btn-refresh-orders");
    
    // Search elements
    const searchIdInput = document.getElementById("search-id");
    const btnSearchOrder = document.getElementById("btn-search-order");
    const searchResult = document.getElementById("search-result");

    // C# Report elements
    const btnLoadCsharpReport = document.getElementById("btn-load-csharp-report");
    const csharpTotalOrders = document.getElementById("csharp-total-orders");
    const csharpReportSystem = document.getElementById("csharp-report-system");
    const csharpTotalRevenue = document.getElementById("csharp-total-revenue");
    const csharpReportTime = document.getElementById("csharp-report-time");
    const csharpDataSource = document.getElementById("csharp-data-source");
    const authSourceIndicator = document.getElementById("auth-source-indicator");

    // --- 1. Tab Navigation System ---
    navItems.forEach(item => {
        item.addEventListener("click", (e) => {
            e.preventDefault();
            const targetId = item.getAttribute("data-target");
            
            // Toggle active menu class
            navItems.forEach(nav => nav.classList.remove("active"));
            item.classList.add("active");
            
            // Toggle active tab pane
            tabPanes.forEach(pane => pane.classList.remove("active"));
            document.getElementById(targetId).classList.add("active");
            
            // Update Page Title
            pageTitle.innerText = item.textContent.trim();

            // Auto fetch data on tab switch
            if (targetId === "users-tab") {
                fetchUsers();
            } else if (targetId === "orders-tab") {
                fetchOrders();
            } else if (targetId === "dashboard-tab") {
                updateDashboardStats();
            }
        });
    });

    // --- 2. Auth Interface Toggle (Login / Register forms) ---
    tabLoginBtn.addEventListener("click", () => {
        tabLoginBtn.classList.add("active");
        tabRegisterBtn.classList.remove("active");
        formLogin.classList.add("active");
        formRegister.classList.remove("active");
        authAlert.classList.add("hidden");
    });

    tabRegisterBtn.addEventListener("click", () => {
        tabRegisterBtn.classList.add("active");
        tabLoginBtn.classList.remove("active");
        formRegister.classList.add("active");
        formLogin.classList.remove("active");
        authAlert.classList.add("hidden");
    });

    // --- 3. API Logic: Login ---
    formLogin.addEventListener("submit", async (e) => {
        e.preventDefault();
        const username = document.getElementById("login-username").value;
        const password = document.getElementById("login-password").value;
        
        showAuthAlert("", "clear");

        try {
            const res = await fetch(`${API_BASE}/auth/login`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ username, password })
            });
            const data = await res.json();
            
            if (data.error) {
                showAuthAlert(data.error, "error");
            } else {
                token = data.token;
                localStorage.setItem("token", token);
                localStorage.setItem("user", JSON.stringify(data.user));
                localStorage.setItem("authSource", data.source || "SQLite Local Database (Fallback)");
                
                currentUser = data.user;
                updateUserProfileUI();
                authSection.classList.add("hidden"); // Hide login panel
                
                // Show success feedback
                updateDashboardStats();
            }
        } catch (err) {
            showAuthAlert("Không thể kết nối đến API server.", "error");
        }
    });

    // --- 4. API Logic: Register ---
    formRegister.addEventListener("submit", async (e) => {
        e.preventDefault();
        const username = document.getElementById("reg-username").value;
        const email = document.getElementById("reg-email").value;
        const password = document.getElementById("reg-password").value;
        
        showAuthAlert("", "clear");

        try {
            const res = await fetch(`${API_BASE}/users`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ username, password, email })
            });
            const data = await res.json();
            
            if (data.error) {
                showAuthAlert(data.error, "error");
            } else {
                showAuthAlert(data.message || "Đăng ký thành công! Hãy đăng nhập.", "success");
                formRegister.reset();
                // Switch back to login form
                tabLoginBtn.click();
            }
        } catch (err) {
            showAuthAlert("Không thể kết nối đến API server.", "error");
        }
    });

    // --- 5. Logout ---
    btnLogout.addEventListener("click", () => {
        localStorage.removeItem("token");
        localStorage.removeItem("user");
        localStorage.removeItem("authSource");
        token = null;
        currentUser = null;
        updateUserProfileUI();
        
        // Show login section again
        authSection.classList.remove("hidden");
        formLogin.reset();
    });

    // --- 6. API Logic: Fetch Users ---
    async function fetchUsers() {
        try {
            const res = await fetch(`${API_BASE}/users`);
            const users = await res.json();
            
            usersTableBody.innerHTML = "";
            userCountBadge.innerText = `${users.length} Users`;
            
            users.forEach(u => {
                const tr = document.createElement("tr");
                tr.innerHTML = `
                    <td>${u.id}</td>
                    <td><strong>${u.username}</strong></td>
                    <td>${u.email}</td>
                    <td><span class="badge ${u.is_admin ? 'admin' : 'user'}">${u.is_admin ? 'ADMIN' : 'USER'}</span></td>
                `;
                usersTableBody.appendChild(tr);
            });
            return users.length;
        } catch (err) {
            console.error("Lỗi lấy danh sách user:", err);
            return 0;
        }
    }

    // --- 7. API Logic: Place Order (Facade) ---
    formOrder.addEventListener("submit", async (e) => {
        e.preventDefault();
        
        if (!token) {
            showOrderAlert("Vui lòng đăng nhập trước khi đặt hàng!", "error");
            return;
        }
        
        const productId = parseInt(document.getElementById("order-product-id").value);
        const orderType = document.querySelector('input[name="order_type"]:checked').value;
        const address = document.getElementById("order-address").value;
        
        showOrderAlert("", "clear");

        try {
            const res = await fetch(`${API_BASE}/orders/place`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ product_id: productId, order_type: orderType, address: address })
            });
            const data = await res.json();
            
            if (data.status === "Success") {
                showOrderAlert(`Đặt hàng thành công! Mã đơn: ${data.order_id}. Mã vận đơn (Facade): ${data.tracking_code}`, "success");
                formOrder.reset();
                fetchOrders(); // Refresh table
            } else {
                showOrderAlert(`Lỗi: ${data.reason}`, "error");
            }
        } catch (err) {
            showOrderAlert("Lỗi kết nối API đặt hàng.", "error");
        }
    });

    // --- 8. API Logic: Fetch Orders (Iterator) ---
    async function fetchOrders() {
        try {
            const res = await fetch(`${API_BASE}/orders/`);
            const orders = await res.json();
            
            ordersTableBody.innerHTML = "";
            orders.forEach(o => {
                const tr = document.createElement("tr");
                
                // Class badge state style
                let badgeClass = "status-pending";
                if (o.status === "Shipped") badgeClass = "status-shipped";
                if (o.status === "Paid") badgeClass = "status-paid";

                tr.innerHTML = `
                    <td>${o.id}</td>
                    <td>${o.details}</td>
                    <td><span class="badge ${badgeClass}">${o.status}</span></td>
                    <td><code>${o.tracking_code}</code></td>
                `;
                ordersTableBody.appendChild(tr);
            });
            return orders;
        } catch (err) {
            console.error("Lỗi lấy danh sách order:", err);
            return [];
        }
    }

    // --- 9. API Logic: Search Order (Iterator) ---
    btnSearchOrder.addEventListener("click", async () => {
        const id = searchIdInput.value.trim();
        if (!id) return;
        
        searchResult.classList.add("hidden");

        try {
            const res = await fetch(`${API_BASE}/orders/search/${id}`);
            const data = await res.json();
            
            searchResult.innerHTML = "";
            searchResult.classList.remove("hidden");

            if (data.error) {
                searchResult.innerHTML = `<div class="alert error-alert"><i class="fa-solid fa-triangle-exclamation"></i> ${data.error}</div>`;
            } else {
                // Class badge state style
                let badgeClass = "status-pending";
                if (data.status === "Shipped") badgeClass = "status-shipped";
                if (data.status === "Paid") badgeClass = "status-paid";

                searchResult.innerHTML = `
                    <div class="result-item">
                        <div class="result-row">
                            <span class="label">Mã đơn hàng:</span>
                            <span class="value">#${data.id}</span>
                        </div>
                        <div class="result-row">
                            <span class="label">Chi tiết sản phẩm:</span>
                            <span class="value">${data.details}</span>
                        </div>
                        <div class="result-row">
                            <span class="label">Trạng thái (State):</span>
                            <span class="value"><span class="badge ${badgeClass}">${data.status}</span></span>
                        </div>
                        <div class="result-row">
                            <span class="label">Mã vận đơn (Facade):</span>
                            <span class="value"><code>${data.tracking_code}</code></span>
                        </div>
                    </div>
                `;
            }
        } catch (err) {
            searchResult.classList.remove("hidden");
            searchResult.innerHTML = `<div class="alert error-alert">Lỗi kết nối khi tìm kiếm.</div>`;
        }
    });

    btnRefreshOrders.addEventListener("click", fetchOrders);
    btnLoadCsharpReport.addEventListener("click", fetchCsharpReport);

    // --- 10. Dashboard Stats Aggregator ---
    async function updateDashboardStats() {
        if (!token) return;
        try {
            // Fetch total users count
            const usersRes = await fetch(`${API_BASE}/users`);
            const users = await usersRes.json();
            dbTotalUsers.innerText = users.length;

            // Fetch orders states
            const ordersRes = await fetch(`${API_BASE}/orders/`);
            const orders = await ordersRes.json();
            
            const pending = orders.filter(o => o.status === "Pending" || o.status === "Paid").length;
            const shipped = orders.filter(o => o.status === "Shipped").length;
            
            dbPendingOrders.innerText = pending;
            dbShippedOrders.innerText = shipped;

            // Tự động tải báo cáo từ C# Microservice
            fetchCsharpReport();
        } catch (err) {
            console.error("Lỗi cập nhật dashboard:", err);
        }
    }

    // --- 11. Fetch C# Microservice Report ---
    async function fetchCsharpReport() {
        if (!token) return;
        
        csharpTotalOrders.innerText = "Loading...";
        csharpTotalRevenue.innerText = "Loading...";
        csharpReportSystem.innerText = "Đang kết nối...";
        csharpDataSource.innerText = "Đang gọi Proxy...";

        try {
            const res = await fetch(`${API_BASE}/report/csharp-summary`);
            const data = await res.json();
            
            if (data.error) {
                csharpTotalOrders.innerText = "Error";
                csharpTotalRevenue.innerText = "Error";
                csharpReportSystem.innerText = "Lỗi phản hồi";
                csharpDataSource.innerText = "N/A";
            } else {
                csharpTotalOrders.innerText = data.total_orders;
                csharpTotalRevenue.innerText = `$${Number(data.total_revenue).toFixed(2)}`;
                csharpReportSystem.innerText = data.system || "C# Microservice";
                csharpDataSource.innerText = data.data_source || "C# Report Service";
                
                // Hiển thị thời gian cập nhật
                const now = new Date();
                csharpReportTime.innerText = `Cập nhật lúc: ${now.toLocaleTimeString()}`;
            }
        } catch (err) {
            console.error("Lỗi lấy báo cáo C#:", err);
            csharpTotalOrders.innerText = "Offline";
            csharpTotalRevenue.innerText = "Offline";
            csharpReportSystem.innerText = "Không thể kết nối C#";
            csharpDataSource.innerText = "FastAPI Local Cache";
        }
    }

    // --- Helper UI functions ---
    function showAuthAlert(msg, type) {
        authAlert.classList.add("hidden");
        authAlert.className = "alert"; // reset classes
        
        if (type === "clear") return;
        
        authAlert.classList.remove("hidden");
        if (type === "error") {
            authAlert.classList.add("error-alert");
            authAlert.innerHTML = `<i class="fa-solid fa-circle-exclamation"></i> ${msg}`;
        } else if (type === "success") {
            authAlert.classList.add("success-alert");
            authAlert.innerHTML = `<i class="fa-solid fa-circle-check"></i> ${msg}`;
        }
    }

    function showOrderAlert(msg, type) {
        orderAlert.classList.add("hidden");
        orderAlert.className = "alert";
        
        if (type === "clear") return;
        
        orderAlert.classList.remove("hidden");
        if (type === "error") {
            orderAlert.classList.add("error-alert");
            orderAlert.innerHTML = `<i class="fa-solid fa-circle-exclamation"></i> ${msg}`;
        } else if (type === "success") {
            orderAlert.classList.add("success-alert");
            orderAlert.innerHTML = `<i class="fa-solid fa-circle-check"></i> ${msg}`;
        }
    }

    function updateUserProfileUI() {
        if (currentUser) {
            userDisplayName.innerText = currentUser.username;
            userDisplayRole.innerText = currentUser.is_admin ? "Administrator" : "User";
            btnLogout.classList.remove("hidden");
            
            const authSource = localStorage.getItem("authSource") || "SQLite Local Database (Fallback)";
            authSourceIndicator.innerText = `Xác thực: ${authSource}`;
        } else {
            userDisplayName.innerText = "Chưa đăng nhập";
            userDisplayRole.innerText = "Khách";
            btnLogout.classList.add("hidden");
            authSourceIndicator.innerText = "Chưa xác thực";
        }
    }

    // --- Init Checking on startup ---
    function init() {
        const storedUser = localStorage.getItem("user");
        if (token && storedUser) {
            currentUser = JSON.parse(storedUser);
            updateUserProfileUI();
            authSection.classList.add("hidden"); // Ẩn panel login
            updateDashboardStats();
        } else {
            updateUserProfileUI();
            authSection.classList.remove("hidden");
        }
    }

    init();
});
