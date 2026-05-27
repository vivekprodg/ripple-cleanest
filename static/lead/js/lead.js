/* =========================================================
   LEAD MANAGEMENT PAGE SCRIPT
   Ripple Architecture / Ripple CRM
   Reusable for all lead HTML files
========================================================= */

(() => {
    const data = [
        {
            id: 1,
            name: "Vivek Mani Upadhyaya",
            email: "vivek.upadhyaya@example.com",
            phone: "+977-9812345678",
            project: "12,000 sq ft Villa",
            location: "Kathmandu, Nepal",
            timeline: "Late 2027",
            source: "RFQ Form",
            sourceKey: "quote",
            type: "quote",
            status: "new",
            priority: "hot",
            budget: "NPR 150M+",
            notes: "Premium villa inquiry. Needs master plan + interiors.",
            tags: ["Architecture", "Residential", "Luxury"],
            avatar: "https://images.unsplash.com/photo-1560250097-0b93528c311a?auto=format&fit=crop&w=150&q=80",
            date: "Today, 10:45 AM"
        },
        {
            id: 2,
            name: "Sarah Jenkins",
            email: "sarah.jenkins@example.com",
            phone: "+977-9801122334",
            project: "Interior Consultation",
            location: "Lalitpur, Nepal",
            timeline: "Next Month",
            source: "Contact Form",
            sourceKey: "contact",
            type: "contact",
            status: "new",
            priority: "warm",
            budget: "NPR 2.5M",
            notes: "Needs premium living room redesign.",
            tags: ["Interior", "Residential", "Renovation"],
            avatar: "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=150&q=80",
            date: "Yesterday"
        },
        {
            id: 3,
            name: "Marcus Reed",
            email: "marcus.reed@example.com",
            phone: "+977-9840011223",
            project: "Commercial Office Space",
            location: "Kathmandu, Nepal",
            timeline: "Q1 2027",
            source: "LinkedIn",
            sourceKey: "linkedin",
            type: "website",
            status: "contacted",
            priority: "hot",
            budget: "NPR 45M",
            notes: "CEO of TechCorp looking for HQ layout.",
            tags: ["Commercial", "Office", "Corporate"],
            avatar: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=150&q=80",
            date: "2 days ago"
        },
        {
            id: 4,
            name: "Elena Rostova",
            email: "elena.rostova@example.com",
            phone: "+977-9867788990",
            project: "Landscape Architecture",
            location: "Pokhara, Nepal",
            timeline: "This Year",
            source: "Facebook",
            sourceKey: "facebook",
            type: "ad",
            status: "contacted",
            priority: "warm",
            budget: "NPR 12M",
            notes: "Facebook ad inquiry for resort landscape.",
            tags: ["Landscape", "Hospitality", "Resort"],
            avatar: "https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&w=150&q=80",
            date: "Last Week"
        },
        {
            id: 5,
            name: "Ankit Shrestha",
            email: "ankit@example.com",
            phone: "+977-9841010101",
            project: "Apartment Renovation",
            location: "Bhaktapur, Nepal",
            timeline: "ASAP",
            source: "WhatsApp",
            sourceKey: "whatsapp",
            type: "whatsapp",
            status: "won",
            priority: "hot",
            budget: "NPR 8M",
            notes: "Converted. Interior renovation project signed.",
            tags: ["Interior", "Apartment", "Renovation"],
            avatar: "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&w=150&q=80",
            date: "Today"
        },
        {
            id: 6,
            name: "Nadine Carter",
            email: "nadine@example.com",
            phone: "+977-9810009998",
            project: "Eco Resort Concept",
            location: "Chitwan, Nepal",
            timeline: "2028",
            source: "Website",
            sourceKey: "website",
            type: "website",
            status: "lost",
            priority: "cold",
            budget: "NPR 60M",
            notes: "Long-term prospect, no response after follow-up.",
            tags: ["Hospitality", "Resort", "Eco"],
            avatar: "https://images.unsplash.com/photo-1488426862026-3ee34a7d66df?auto=format&fit=crop&w=150&q=80",
            date: "3 weeks ago"
        }
    ];

    let selectedCard = null;
    let currentLeadId = null;

    const sourceClassMap = {
        quote: "source-quote",
        contact: "source-contact",
        website: "source-website",
        ad: "source-fb",
        facebook: "source-fb",
        linkedin: "source-li",
        whatsapp: "source-whatsapp"
    };

    const statusClassMap = {
        new: "status-new",
        contacted: "status-contacted",
        won: "status-won",
        lost: "status-lost"
    };

    const priorityClassMap = {
        hot: "priority-hot",
        warm: "priority-warm",
        cold: "priority-cold"
    };

    function badgeLabelFromStatus(status) {
        return String(status || "")
            .charAt(0)
            .toUpperCase() + String(status || "").slice(1);
    }

    function escapeHtml(text) {
        return String(text ?? "")
            .replaceAll("&", "&amp;")
            .replaceAll("<", "&lt;")
            .replaceAll(">", "&gt;")
            .replaceAll('"', "&quot;")
            .replaceAll("'", "&#039;");
    }

    function cardTemplate(lead) {
        const tagsHtml = (lead.tags || [])
            .map(tag => `<span class="tag">${escapeHtml(tag)}</span>`)
            .join("");

        return `
            <div class="card" draggable="true"
                 data-id="${lead.id}"
                 data-name="${escapeHtml(lead.name)}"
                 data-email="${escapeHtml(lead.email)}"
                 data-phone="${escapeHtml(lead.phone)}"
                 data-project="${escapeHtml(lead.project)}"
                 data-location="${escapeHtml(lead.location)}"
                 data-timeline="${escapeHtml(lead.timeline)}"
                 data-source="${escapeHtml(lead.source)}"
                 data-source-key="${escapeHtml(lead.sourceKey)}"
                 data-type="${escapeHtml(lead.type)}"
                 data-status="${escapeHtml(lead.status)}"
                 data-priority="${escapeHtml(lead.priority)}"
                 data-budget="${escapeHtml(lead.budget)}"
                 data-notes="${escapeHtml(lead.notes)}"
                 data-tags="${escapeHtml((lead.tags || []).join(", "))}"
                 onclick="openInspectorByCard(this)">
                <div class="card-header">
                    <div class="client-info">
                        <img src="${lead.avatar}" alt="Client" class="avatar">
                        <div class="client-text">
                            <div class="client-name">${escapeHtml(lead.name)}</div>
                            <div class="client-date">${escapeHtml(lead.date)}</div>
                        </div>
                    </div>
                    <div class="badges">
                        <span class="status-badge ${statusClassMap[lead.status] || statusClassMap.new}">${badgeLabelFromStatus(lead.status)}</span>
                        <span class="priority-badge ${priorityClassMap[lead.priority] || priorityClassMap.cold}">${String(lead.priority || "cold").toUpperCase()}</span>
                        <span class="source-badge ${sourceClassMap[lead.sourceKey] || "source-website"}">${escapeHtml(lead.source)}</span>
                    </div>
                </div>

                <div class="card-body">
                    <p><strong>Type:</strong> ${escapeHtml(lead.project)}</p>
                    <p><strong>Location:</strong> ${escapeHtml(lead.location)}</p>
                    <p><strong>Timeline:</strong> ${escapeHtml(lead.timeline)}</p>
                    <div class="tag-row">${tagsHtml}</div>
                </div>

                <div class="card-footer">
                    <span class="budget">${escapeHtml(lead.budget)}</span>
                    <div class="actions">
                        <i class="fas fa-phone" title="Call"></i>
                        <i class="fas fa-envelope" title="Email"></i>
                        <i class="fas fa-comment-dots" title="Note"></i>
                    </div>
                </div>
            </div>
        `;
    }

    function getEl(id) {
        return document.getElementById(id);
    }

    function renderBoard() {
        const columns = {
            new: document.querySelector("#col-new .cards-container"),
            contacted: document.querySelector("#col-contacted .cards-container"),
            won: document.querySelector("#col-won .cards-container"),
            lost: document.querySelector("#col-lost .cards-container")
        };

        if (!columns.new && !columns.contacted && !columns.won && !columns.lost) return;

        Object.values(columns).forEach(col => {
            if (col) col.innerHTML = "";
        });

        data.forEach(lead => {
            const container = columns[lead.status] || columns.new;
            if (container) {
                container.insertAdjacentHTML("beforeend", cardTemplate(lead));
            }
        });

        attachCardEvents();
        updateCounts();
        applyFilters();
    }

    function attachCardEvents() {
        document.querySelectorAll(".card").forEach(card => {
            card.addEventListener("dragstart", () => {
                selectedCard = card;
                card.classList.add("dragging");
            });

            card.addEventListener("dragend", () => {
                card.classList.remove("dragging");
                selectedCard = null;
                syncLeadFromDOM(card);
                updateCounts();
            });
        });

        document.querySelectorAll(".cards-container").forEach(container => {
            container.addEventListener("dragover", e => {
                e.preventDefault();
                container.classList.add("drag-over");
                const afterElement = getDragAfterElement(container, e.clientY);
                if (!selectedCard) return;

                if (afterElement == null) {
                    container.appendChild(selectedCard);
                } else {
                    container.insertBefore(selectedCard, afterElement);
                }
            });

            container.addEventListener("dragleave", () => {
                container.classList.remove("drag-over");
            });

            container.addEventListener("drop", () => {
                container.classList.remove("drag-over");
                if (!selectedCard) return;

                const status = container.dataset.status;
                const leadId = Number(selectedCard.dataset.id);
                const lead = data.find(x => x.id === leadId);

                if (lead) {
                    lead.status = status;
                    if (status === "won") lead.priority = "hot";
                    if (status === "lost") lead.priority = "cold";

                    selectedCard.dataset.status = status;
                    selectedCard.dataset.priority = lead.priority;

                    const statusBadge = selectedCard.querySelector(".status-badge");
                    const priorityBadge = selectedCard.querySelector(".priority-badge");

                    if (statusBadge) {
                        statusBadge.className = `status-badge ${statusClassMap[status] || statusClassMap.new}`;
                        statusBadge.textContent = badgeLabelFromStatus(status);
                    }

                    if (priorityBadge) {
                        priorityBadge.className = `priority-badge ${priorityClassMap[lead.priority] || priorityClassMap.cold}`;
                        priorityBadge.textContent = String(lead.priority).toUpperCase();
                    }

                    syncLeadFromDOM(selectedCard);
                }

                updateCounts();
                applyFilters();
            });
        });
    }

    function getDragAfterElement(container, y) {
        const draggableElements = [...container.querySelectorAll(".card:not(.dragging)")];

        return draggableElements.reduce((closest, child) => {
            const box = child.getBoundingClientRect();
            const offset = y - box.top - box.height / 2;

            if (offset < 0 && offset > closest.offset) {
                return { offset, element: child };
            }
            return closest;
        }, { offset: Number.NEGATIVE_INFINITY }).element;
    }

    function updateCounts() {
        const counters = {
            new: data.filter(x => x.status === "new").length,
            contacted: data.filter(x => x.status === "contacted").length,
            won: data.filter(x => x.status === "won").length,
            lost: data.filter(x => x.status === "lost").length
        };

        const countNew = getEl("count-new");
        const countContacted = getEl("count-contacted");
        const countWon = getEl("count-won");
        const countLost = getEl("count-lost");

        const statNew = getEl("stat-new");
        const statContacted = getEl("stat-contacted");
        const statWon = getEl("stat-won");
        const statConv = getEl("stat-conv");

        if (countNew) countNew.textContent = counters.new;
        if (countContacted) countContacted.textContent = counters.contacted;
        if (countWon) countWon.textContent = counters.won;
        if (countLost) countLost.textContent = counters.lost;

        if (statNew) statNew.textContent = counters.new;
        if (statContacted) statContacted.textContent = counters.contacted;
        if (statWon) statWon.textContent = counters.won;

        const total = data.length || 1;
        const conv = Math.round((counters.won / total) * 100);
        if (statConv) statConv.textContent = `${conv}%`;
    }

    function syncLeadFromDOM(card) {
        const id = Number(card.dataset.id);
        const lead = data.find(x => x.id === id);
        if (!lead) return;

        lead.status = card.dataset.status;
        lead.priority = card.dataset.priority;
    }

    function openInspectorByCard(card) {
        if (!card) return;

        document.querySelectorAll(".card").forEach(c => c.classList.remove("selected"));
        card.classList.add("selected");
        currentLeadId = Number(card.dataset.id);

        const inspector = getEl("inspector");
        if (inspector) inspector.style.display = "block";

        const mappings = [
            ["i-name", card.dataset.name],
            ["i-email", card.dataset.email],
            ["i-phone", card.dataset.phone],
            ["i-project", card.dataset.project],
            ["i-location", card.dataset.location],
            ["i-source", card.dataset.source]
        ];

        mappings.forEach(([id, value]) => {
            const el = getEl(id);
            if (el) el.innerText = value || "-";
        });

        const status = getEl("i-status");
        const priority = getEl("i-priority");
        const tags = getEl("i-tags");
        const notes = getEl("i-notes");

        if (status) status.value = card.dataset.status || "new";
        if (priority) priority.value = card.dataset.priority || "cold";
        if (tags) tags.value = card.dataset.tags || "";
        if (notes) notes.value = card.dataset.notes || "";
    }

    function closeInspector() {
        const inspector = getEl("inspector");
        if (inspector) inspector.style.display = "none";

        document.querySelectorAll(".card").forEach(c => c.classList.remove("selected"));
        currentLeadId = null;
    }

    function saveInspector() {
        if (!currentLeadId) return;

        const lead = data.find(x => x.id === currentLeadId);
        const card = document.querySelector(`.card[data-id="${currentLeadId}"]`);
        if (!lead || !card) return;

        const newStatus = getEl("i-status")?.value || "new";
        const newPriority = getEl("i-priority")?.value || "cold";
        const newTagsValue = getEl("i-tags")?.value || "";
        const newNotes = getEl("i-notes")?.value || "";

        lead.status = newStatus;
        lead.priority = newPriority;
        lead.tags = newTagsValue
            .split(",")
            .map(t => t.trim())
            .filter(Boolean);
        lead.notes = newNotes;

        card.dataset.status = lead.status;
        card.dataset.priority = lead.priority;
        card.dataset.tags = lead.tags.join(", ");
        card.dataset.notes = lead.notes;

        const statusBadge = card.querySelector(".status-badge");
        const priorityBadge = card.querySelector(".priority-badge");

        if (statusBadge) {
            statusBadge.className = `status-badge ${statusClassMap[lead.status] || statusClassMap.new}`;
            statusBadge.textContent = badgeLabelFromStatus(lead.status);
        }

        if (priorityBadge) {
            priorityBadge.className = `priority-badge ${priorityClassMap[lead.priority] || priorityClassMap.cold}`;
            priorityBadge.textContent = String(lead.priority).toUpperCase();
        }

        lead.tags = lead.tags.length ? lead.tags : ["Lead"];

        renderBoard();
        const refreshedCard = document.querySelector(`.card[data-id="${currentLeadId}"]`);
        if (refreshedCard) openInspectorByCard(refreshedCard);
        applyFilters();
    }

    function simulateCall() {
        alert("Call action placeholder. Connect this to staff phone workflow.");
    }

    function simulateEmail() {
        alert("Email action placeholder. Connect this to lead email workflow.");
    }

    function openModal() {
        const backdrop = getEl("modalBackdrop");
        if (backdrop) backdrop.style.display = "flex";
    }

    function closeModal() {
        const backdrop = getEl("modalBackdrop");
        const form = getEl("addLeadForm");

        if (backdrop) backdrop.style.display = "none";
        if (form) form.reset();
    }

    function getSourceLabel(sourceKey) {
        const sourceLabelMap = {
            website: "Website",
            quote: "RFQ Form",
            contact: "Contact Form",
            facebook: "Facebook",
            linkedin: "LinkedIn",
            whatsapp: "WhatsApp"
        };
        return sourceLabelMap[sourceKey] || "Website";
    }

    function applyFilters() {
        const search = (getEl("searchInput")?.value || "").toLowerCase().trim();
        const type = getEl("filterType")?.value || "";
        const status = getEl("filterStatus")?.value || "";
        const priority = getEl("filterPriority")?.value || "";
        const source = getEl("filterSource")?.value || "";

        document.querySelectorAll(".card").forEach(card => {
            const haystack = [
                card.dataset.name,
                card.dataset.email,
                card.dataset.project,
                card.dataset.location,
                card.dataset.source,
                card.dataset.tags,
                card.dataset.notes
            ].join(" ").toLowerCase();

            const matchSearch = !search || haystack.includes(search);
            const matchType = !type || card.dataset.type === type;
            const matchStatus = !status || card.dataset.status === status;
            const matchPriority = !priority || card.dataset.priority === priority;
            const matchSource = !source || card.dataset.sourceKey === source || String(card.dataset.source || "").toLowerCase() === source;

            card.style.display = (matchSearch && matchType && matchStatus && matchPriority && matchSource) ? "" : "none";
        });
    }

    function resetFilters() {
        const search = getEl("searchInput");
        const type = getEl("filterType");
        const status = getEl("filterStatus");
        const priority = getEl("filterPriority");
        const source = getEl("filterSource");

        if (search) search.value = "";
        if (type) type.value = "";
        if (status) status.value = "";
        if (priority) priority.value = "";
        if (source) source.value = "";

        applyFilters();
    }

    function handleAddLeadSubmit(e) {
        e.preventDefault();

        const name = getEl("new-name")?.value.trim() || "";
        const email = getEl("new-email")?.value.trim() || "";
        const phone = getEl("new-phone")?.value.trim() || "";
        const type = getEl("new-type")?.value || "quote";
        const status = getEl("new-status")?.value || "new";
        const priority = getEl("new-priority")?.value || "cold";
        const sourceKey = getEl("new-source")?.value || "website";

        const nextId = data.length ? Math.max(...data.map(x => x.id)) + 1 : 1;

        const newLead = {
            id: nextId,
            name,
            email,
            phone,
            project: getEl("new-project")?.value.trim() || "Project Inquiry",
            location: getEl("new-location")?.value.trim() || "-",
            timeline: getEl("new-timeline")?.value.trim() || "-",
            source: getSourceLabel(sourceKey),
            sourceKey,
            type,
            status,
            priority,
            budget: getEl("new-budget")?.value.trim() || "-",
            notes: getEl("new-notes")?.value.trim() || "",
            tags: (getEl("new-tags")?.value || "")
                .split(",")
                .map(t => t.trim())
                .filter(Boolean),
            avatar: "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&w=150&q=80",
            date: "Just now"
        };

        data.unshift(newLead);
        renderBoard();
        closeModal();

        const card = document.querySelector(`.card[data-id="${newLead.id}"]`);
        if (card) openInspectorByCard(card);
    }

    async function handleNewsletterSubmit(e) {
        e.preventDefault();

        const form = e.currentTarget;
        const emailInput = form.querySelector("input[name='email']");
        if (!emailInput) return;

        const email = String(emailInput.value || "").trim();
        if (!email) {
            alert("Email is required.");
            return;
        }

        try {
            const formData = new FormData(form);
            const csrfToken = form.querySelector("[name=csrfmiddlewaretoken]")?.value || "";

            const response = await fetch(form.action, {
                method: "POST",
                body: formData,
                headers: {
                    "X-CSRFToken": csrfToken,
                    "Accept": "application/json"
                }
            });

            let dataResponse = null;
            try {
                dataResponse = await response.json();
            } catch (jsonError) {
                dataResponse = null;
            }

            if (!response.ok) {
                alert((dataResponse && dataResponse.message) || "Subscription failed");
                return;
            }

            alert((dataResponse && dataResponse.message) || "Subscribed successfully");
            form.reset();
        } catch (error) {
            alert("Subscription failed");
        }
    }

    function bindEvents() {
        const form = getEl("addLeadForm");
        if (form) {
            form.addEventListener("submit", handleAddLeadSubmit);
        }

        const backdrop = getEl("modalBackdrop");
        if (backdrop) {
            backdrop.addEventListener("click", function (e) {
                if (e.target === this) closeModal();
            });
        }

        const search = getEl("searchInput");
        const type = getEl("filterType");
        const status = getEl("filterStatus");
        const priority = getEl("filterPriority");
        const source = getEl("filterSource");

        if (search) search.addEventListener("input", applyFilters);
        if (type) type.addEventListener("change", applyFilters);
        if (status) status.addEventListener("change", applyFilters);
        if (priority) priority.addEventListener("change", applyFilters);
        if (source) source.addEventListener("change", applyFilters);

        const newsletterForm = document.querySelector(".newsletter-form");
        if (newsletterForm) {
            newsletterForm.addEventListener("submit", handleNewsletterSubmit);
        }
    }

    // Expose functions used by inline HTML handlers
    window.openInspectorByCard = openInspectorByCard;
    window.closeInspector = closeInspector;
    window.saveInspector = saveInspector;
    window.simulateCall = simulateCall;
    window.simulateEmail = simulateEmail;
    window.openModal = openModal;
    window.closeModal = closeModal;
    window.applyFilters = applyFilters;
    window.resetFilters = resetFilters;

    document.addEventListener("DOMContentLoaded", () => {
        bindEvents();
        renderBoard();
        updateCounts();
        applyFilters();
    });
})();