# Availability Tracking System - Complete Guide

## 🎯 Overview

The **Availability Tracking System** replaces fake hardcoded numbers with REAL tracking of:
- ✅ Limited sponsorship tiers (Captain's Helm, Bar Captain)
- ✅ Ticket capacity remaining
- ✅ Dynamic warning alerts on website
- ✅ Real-time updates via Admin Panel

**No more fake data like "127 of 160" or "Bar Captain (2 of 3 remaining)"**

---

## 📊 What Gets Tracked

### **Limited Tiers** (Maximum Slots)
```
Captain's Helm        → Max: 1 slot
Bar Captain          → Max: 3 slots
```

### **Other Metrics** (Unlimited but tracked)
```
Tickets              → Max: 160 seats
All other sponsors   → Unlimited (track for reporting)
```

---

## 🔄 How It Works

### **Step 1: Update Admin Panel**
Go to: `https://allhandsondecknhn.netlify.app/#admin-panel`

Enter these values:
```
LIMITED TIER AVAILABILITY section:
├─ Captain's Helm Sold: [Enter number who bought it]
└─ Bar Captain Sold: [Enter number who bought it]

TICKET SALES section:
└─ Tickets Sold: [Enter total tickets sold]
```

### **Step 2: System Calculates Remaining**
```
Captain's Helm Remaining = 1 - [sold]
Example: 1 - 1 = 0 remaining (SOLD OUT)

Bar Captain Remaining = 3 - [sold]
Example: 3 - 1 = 2 remaining (LIMITED)

Tickets Remaining = 160 - [sold]
Example: 160 - 127 = 33 remaining
```

### **Step 3: Website Updates Automatically**
```
If Captain's Helm = 0 remaining:
  Display: "Captain's Helm - SOLD OUT ❌"
  Color: Red
  Hide from purchase options

If Bar Captain = 1-2 remaining:
  Display: "Bar Captain (2 of 3 remaining)"
  Color: Yellow/Orange
  Show warning alert

If Tickets < 34 remaining:
  Display: "Only 33 seats remaining"
  Color: Yellow/Orange
  Show urgency alert
```

---

## 📋 Daily Update Routine

### **Time: 3:00 PM Daily**

**Step 1: Check Sales**
```
From Donorbox / Tracking Sheet:
├─ How many new sponsorships sold?
├─ Which tiers were purchased?
├─ How many new tickets?
└─ Any limited tiers sold?
```

**Step 2: Open Admin Panel**
```
URL: https://allhandsondecknhn.netlify.app/#admin-panel
```

**Step 3: Update Limited Tiers**
```
If Captain's Helm sold:
  Update: "Captain's Helm Sold" = 1
  
If Bar Captain sold:
  Update: "Bar Captain Sold" = [new count]
  Examples:
  ├─ First Bar Captain: 1
  ├─ Second Bar Captain: 2
  └─ Third Bar Captain: 3
```

**Step 4: Update Tickets**
```
Update: "Tickets Sold" = [total count]
Example: 127 (or whatever your current count is)
```

**Step 5: Click Save**
```
Button: "💾 Save & Update Live Site"
↓
See confirmation showing:
├─ Captain's Helm status
├─ Bar Captain status
├─ Tickets remaining
└─ Website updates automatically!
```

**Step 6: Verify Website**
```
Visit: https://allhandsondecknhn.netlify.app/
Scroll to: Sponsorship section
Check: Availability alert is correct
```

---

## 🎯 Example Scenarios

### **Scenario 1: Captain's Helm Sells**
```
BEFORE:
├─ Captain's Helm Sold: 0
└─ Website shows: "Available now"

NEW SALE HAPPENS

ACTION:
├─ Open Admin Panel
├─ Update "Captain's Helm Sold" = 1
└─ Click Save

AFTER:
├─ Captain's Helm Sold: 1
├─ Remaining = 0
├─ Status = "SOLD OUT"
└─ Website shows: "Captain's Helm - SOLD OUT ❌"
```

### **Scenario 2: First Bar Captain Sells**
```
BEFORE:
├─ Bar Captain Sold: 0
└─ Website shows: Available

SALE HAPPENS

ACTION:
├─ Open Admin Panel
├─ Update "Bar Captain Sold" = 1
└─ Click Save

AFTER:
├─ Bar Captain Sold: 1
├─ Remaining = 2 (3-1)
├─ Status = "LIMITED"
└─ Website shows: "⚠️ Bar Captain (2 of 3 remaining)"
```

### **Scenario 3: All Three Bar Captains Sell**
```
PROGRESSION:
├─ Sold: 0 → Remaining: 3 → Status: "Available"
├─ Sold: 1 → Remaining: 2 → Status: "LIMITED" ⚠️
├─ Sold: 2 → Remaining: 1 → Status: "LIMITED" ⚠️
└─ Sold: 3 → Remaining: 0 → Status: "SOLD OUT" ❌
```

### **Scenario 4: Tickets Running Low**
```
PROGRESSION:
├─ Sold: 127 → Remaining: 33 → Show urgency
├─ Sold: 150 → Remaining: 10 → Show BIG warning
├─ Sold: 155 → Remaining: 5 → LAST CHANCE
└─ Sold: 160 → Remaining: 0 → SOLD OUT

Website Alert Changes:
├─ 33 remaining: Yellow warning
├─ 10 remaining: Red warning
└─ 0 remaining: SOLD OUT (remove from site)
```

---

## 📊 Tracking Spreadsheet

Use `Availability_Tracking.csv` to maintain records:

**Columns to fill daily:**
```
Date: [Today's date]
Captain's Helm Sold: [Count]
Bar Captain Sold: [Count]
Total Sponsors Sold: [Count]
Tickets Sold: [Count]
Total Capacity Remaining: [160 - sold]
```

**Example entries:**
```
Date          | C.Helm | Bar Cap | Sponsors | Tickets | Remaining
6/10/2026     | 0      | 0       | 0        | 0       | 160
6/11/2026     | 0      | 0       | 0        | 5       | 155
6/12/2026     | 0      | 1       | 2        | 12      | 148
6/13/2026     | 1      | 1       | 4        | 20      | 140
6/14/2026     | 1      | 2       | 6        | 35      | 125
```

**Use this to verify Admin Panel is accurate!**

---

## 🎨 Website Display Examples

### **When Everything is Available**
```
(No warning banner shown)

SPONSORSHIP TIERS display normally
├─ Captain's Helm: $5,000 - [SELECT]
├─ Bar Captain: $2,000 - [SELECT]
├─ Band Sponsor: $3,000 - [SELECT]
└─ etc.

TICKETS section:
127 of 160 tickets sold (79.4%)
```

### **When Limited Tiers Show**
```
⚠️ LIMITED AVAILABILITY
⚠️ Captain's Helm (1 remaining) •
⚠️ Bar Captain (2 of 3 remaining) •
Secure your tier now!

SPONSORSHIP TIERS display with badges:
├─ ❌ Captain's Helm: SOLD OUT (can't select)
├─ ⚠️  Bar Captain (2 remaining): $2,000 - [SELECT FAST]
└─ ✓ Other tiers: Normal pricing
```

### **When Sold Out**
```
⚠️ LIMITED AVAILABILITY
❌ Captain's Helm: SOLD OUT •
⚠️ Bar Captain (1 of 3 remaining) •
⚠️ Tickets (5 remaining)

SPONSORSHIP SECTION removes SOLD OUT options
TICKETS section shows: "Only 5 seats left!"
```

---

## 👥 Team Responsibilities

### **Michael Franks (Event Chair)**
- Update tickets sold daily
- Monitor overall capacity
- Send team alerts when limited

### **Dolf May (Sponsorship Chair)**
- Update Captain's Helm when sold
- Update Bar Captain count as they sell
- Prioritize these limited tiers

### **Rod Dennis (Director)**
- Oversee all updates
- Verify accuracy daily
- Send email alerts to team

### **Brendan Cassin (Treasurer)**
- Verify sales match revenue
- Reconcile sponsorship numbers
- Keep tracking spreadsheet updated

---

## 📧 Weekly Email Template

```
SUBJECT: All Hands on Deck - Availability Update

Hi Team!

Here's this week's availability status:

LIMITED AVAILABILITY ALERTS:
┌─────────────────────────────────────┐
│ ⚠️  Captain's Helm: 1 REMAINING     │
│ ⚠️  Bar Captain: 2 of 3 REMAINING  │
│ ✓ All others: Available             │
└─────────────────────────────────────┘

CAPACITY STATUS:
├─ Tickets: 127/160 sold (33 remaining)
├─ At 79.4% capacity
└─ On track to sell out

NEXT STEPS:
├─ Push Captain's Helm final sale
├─ Promote Bar Captain availability
└─ Encourage ticket sales

Admin Panel: https://allhandsondecknhn.netlify.app/#admin-panel

Questions? Email Rod Dennis
```

---

## 🔍 Verification Checklist

**Daily (before 4 PM):**
- [ ] Check Donorbox for new sales
- [ ] Update Admin Panel with accurate numbers
- [ ] Click "Save & Update Live Site"
- [ ] Verify website shows correct availability
- [ ] If changes, email team alert

**Weekly (Every Friday):**
- [ ] Compare Admin Panel numbers to tracking sheet
- [ ] Verify all tier counts are accurate
- [ ] Send team email update
- [ ] Celebrate milestones

**Monthly:**
- [ ] Create backup of tracking data
- [ ] Reconcile all numbers
- [ ] Archive previous month's data
- [ ] Plan next month's strategy

---

## ⚠️ Important Notes

### **Don't Do:**
❌ Guess at numbers
❌ Use last month's data
❌ Leave Admin Panel stale
❌ Mix up sponsorship tiers
❌ Forget to update both places (Admin Panel + Spreadsheet)

### **Do:**
✅ Update from actual sales records
✅ Use current data only
✅ Update Admin Panel daily
✅ Double-check tier names
✅ Keep spreadsheet in sync

---

## 🚨 Common Issues & Fixes

### **Problem: Website shows old numbers**
**Solution:**
- Refresh browser (Ctrl+F5)
- Clear cache if needed
- Verify Admin Panel was saved
- Check that you clicked "Save & Update Live Site"

### **Problem: Availability banner not showing**
**Solution:**
- Admin Panel data exists
- Availability numbers are > 0
- Website loaded properly
- Try refreshing page

### **Problem: Numbers don't match spreadsheet**
**Solution:**
- Open Admin Panel
- Compare to tracking spreadsheet
- Find discrepancy
- Update Admin Panel to correct number
- Re-save

### **Problem: Can't remember what we've sold**
**Solution:**
- Check tracking spreadsheet
- Or check Donorbox dashboard
- Update Admin Panel from confirmed source
- Never guess!

---

## 📞 Support

**Questions about availability tracking?**
- Email: rod@roddennis.com
- Phone: 480-695-0733

**Technical issues?**
- Refresh page
- Clear browser cache
- Try different browser

---

## 🎓 Learn More

For more details:
- `ADMIN_PANEL_QUICK_START.txt` - How to use Admin Panel
- `ADMIN_PANEL_GUIDE.md` - Complete Admin Panel guide
- `Availability_Tracking.csv` - Track in spreadsheet
- `QUICK_REFERENCE.txt` - Quick lookup

---

## ✅ You're Ready!

You now have:
- ✓ Real data tracking (no fake numbers)
- ✓ Dynamic website updates
- ✓ Limited tier management
- ✓ Team coordination system
- ✓ Transparent availability

**Admin Panel:** https://allhandsondecknhn.netlify.app/#admin-panel

**Start using it today!**

---

**Last Updated:** June 10, 2026
**Status:** ✅ Ready to Use
**Support:** rod@roddennis.com
