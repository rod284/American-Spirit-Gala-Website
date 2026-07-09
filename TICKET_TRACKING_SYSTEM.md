# Ticket Tracking System - Real Numbers Only

## 🎯 Overview

A comprehensive system to track ACTUAL ticket sales with NO fake data:
- ✅ Starts at ZERO
- ✅ Updates only from real sales
- ✅ Displays live on website
- ✅ Easy daily updates
- ✅ Transparent tracking

---

## 📊 The System

### **Where Ticket Data Is Entered:**
```
ADMIN PANEL → https://allhandsondecknhn.netlify.app/#admin-panel

Section: "🎟️ Ticket Sales"
Field: "Tickets Sold (0-160)"
```

### **How Website Display Updates:**
```
Website shows:
├─ Tickets Sold: [Your number] / 160
├─ Remaining: 160 - [Your number]
├─ Capacity %: ([Your number] ÷ 160) × 100
└─ Updated automatically when you save
```

### **Current Status:**
```
Tickets Sold: 0
Remaining: 160
Capacity: 0%

(Starts at zero - you fill in REAL numbers)
```

---

## 🔄 Daily Update Process

### **Step 1: Get Actual Count (Daily at 3 PM)**
```
Source: Donorbox Dashboard
├─ Go to: https://donorbox.org/nhn-2026-gala-tickets
├─ Check: "Total Tickets Sold"
└─ Note: The number
```

### **Step 2: Open Admin Panel**
```
https://allhandsondecknhn.netlify.app/#admin-panel
```

### **Step 3: Update Tickets Field**
```
Section: "🎟️ TICKET SALES"
Field: "Tickets Sold (0-160)"

Enter: [Actual count from Donorbox]
Example: 127
```

### **Step 4: Save**
```
Click: "💾 Save & Update Live Site"

System calculates:
├─ Remaining = 160 - [your number]
├─ Capacity % = ([your number] ÷ 160) × 100
└─ Website updates automatically
```

### **Step 5: Verify Website**
```
https://allhandsondecknhn.netlify.app

Scroll to: Sponsorship section
Check: "🎟️ Event Capacity" shows correct number
```

---

## 📋 Ticket Sources (Where Numbers Come From)

### **Primary Source: Donorbox**
```
URL: https://donorbox.org/nhn-2026-gala-tickets
├─ Shows real-time sales
├─ Shows total tickets sold
├─ Shows revenue
└─ Most accurate source
```

### **Backup Sources:**
```
Google Forms responses (if using form)
Email confirmations
Cash sales log
In-person registrations
```

### **How to Find Count:**
```
Donorbox Dashboard:
1. Log in to Donorbox
2. Click on campaign: "nhn-2026-gala-tickets"
3. Look for: "Total Donations" or "Total Raised"
4. Divide by $50 = Number of tickets
   Example: $6,350 ÷ $50 = 127 tickets

OR: Look for "Quantity Purchased" if tracked
```

---

## 📊 Real-Time Tracking Spreadsheet

Create a spreadsheet to log daily:

```
Date       | Donorbox Check | Tickets Sold | Remaining | Capacity % | Updated? | Notes
-----------|----------------|--------------|-----------|------------|----------|----------
6/10/2026  | 0              | 0            | 160       | 0%         | ✓        | Started
6/11/2026  | 5              | 5            | 155       | 3%         | ✓        | First sales!
6/12/2026  | 12             | 12           | 148       | 7.5%       | ✓        | 
6/13/2026  | 20             | 20           | 140       | 12.5%      | ✓        | 
6/14/2026  | 35             | 35           | 125       | 22%        | ✓        | Growing!
```

**Columns to track:**
- Date
- Number in Donorbox
- Total tickets updated in Admin Panel
- Seats remaining (160 - sold)
- Capacity percentage
- Updated (yes/no)
- Notes

---

## 🎯 Real Example Scenario

### **Tuesday, June 11, 2026**

**3:00 PM:**
```
Michael checks Donorbox
Sees: $250 in donations for tickets
Calculation: $250 ÷ $50 = 5 tickets sold
```

**3:05 PM:**
```
Opens Admin Panel:
https://allhandsondecknhn.netlify.app/#admin-panel

Finds: "🎟️ Ticket Sales" section
Field: "Tickets Sold (0-160)"
Enters: 5
Clicks: "💾 Save & Update Live Site"
```

**Confirmation popup shows:**
```
✅ Data saved and updated!

Tickets: 5/160
Sponsors: 0 tiers
Revenue: $250

Website will update automatically!
```

**3:10 PM:**
```
Website now displays:
🎟️ Event Capacity
5 of 160 tickets sold • Only 155 seats remaining • 3% capacity
```

**Tracking spreadsheet updated:**
```
Date: 6/11/2026 | Tickets: 5 | Remaining: 155 | Capacity: 3% | Updated: ✓
```

---

## ✅ Daily Checklist

**Every Day at 3:00 PM:**

- [ ] Check Donorbox dashboard
- [ ] Note total tickets sold
- [ ] Open Admin Panel
- [ ] Update "Tickets Sold" field
- [ ] Click Save
- [ ] See confirmation
- [ ] Verify website shows correct number
- [ ] Update tracking spreadsheet
- [ ] Email any alerts to team (if sold >100 or <20 remaining)

**Time required: 5 minutes**

---

## 📊 Display on Website

### **What Visitors See (Updates Automatically):**

#### **Current (Zero):**
```
🎟️ Event Capacity

0 of 160 tickets sold
Only 160 seats remaining
0% capacity
```

#### **After You Update to 35:**
```
🎟️ Event Capacity

35 of 160 tickets sold
Only 125 seats remaining
22% capacity
```

#### **When Close to Full (140+ sold):**
```
🎟️ Event Capacity

145 of 160 tickets sold
Only 15 seats remaining
91% capacity

⚠️ ALMOST SOLD OUT - LAST CHANCE!
```

#### **When Sold Out (160 sold):**
```
🎟️ Event Capacity

160 of 160 tickets sold
Sold Out!
100% capacity

❌ NO SEATS REMAINING
```

---

## 🚨 Urgency Alerts

Website automatically shows warnings:

```
REMAINING > 100  →  No warning (plenty of seats)
REMAINING 50-100 →  No warning (good progress)
REMAINING 33-49  →  Show "Only X remaining" (normal)
REMAINING 20-32  →  Yellow ⚠️ "Only X seats left!"
REMAINING 10-19  →  Red ⚠️ "LAST CHANCE - X seats!"
REMAINING 0-9    →  Red ❌ "ALMOST SOLD OUT"
REMAINING 0      →  Red ❌ "SOLD OUT"
```

---

## 📞 Ticket Sales Sources

### **Official Ticket URL:**
```
https://donorbox.org/nhn-2026-gala-tickets

Share this link for:
├─ Social media posts
├─ Email campaigns
├─ Website
├─ Print materials
└─ Word of mouth
```

### **Tracking Multiple Sources:**
```
If you have multiple ways to buy tickets:

Donorbox (online)    → Primary count
Paper forms (in-person) → Add to total
Phone orders         → Add to total
Email confirmations  → Add to total

Sum them all = Total tickets sold
```

---

## 💰 Revenue Calculation

```
Tickets Sold × $50 = Total Revenue

Examples:
├─ 5 tickets × $50 = $250
├─ 35 tickets × $50 = $1,750
├─ 127 tickets × $50 = $6,350
└─ 160 tickets × $50 = $8,000
```

**Update Admin Panel with this revenue too:**
```
In "💰 REVENUE BREAKDOWN" section:
Field: "Tickets Total Revenue ($)"
Enter: [Tickets Sold × $50]
```

---

## 📈 Projected Milestones

```
MILESTONE          | GOAL        | TARGET DATE | STATUS
-------------------|-------------|-------------|--------
First 25 tickets   | Test sales  | June 30     | TBD
50 tickets         | 31% sold    | July 15     | TBD
100 tickets        | 63% sold    | August 15   | TBD
150 tickets        | 94% sold    | October 15  | TBD
160 tickets (SOLD) | 100%        | Nov 12      | TBD
```

**When you hit milestones:**
- Send email to team
- Post on social media
- Celebrate progress
- Intensify promotion if behind

---

## 📧 Automated Team Alerts

**Send email when:**

```
✅ First ticket sells
   Subject: First ticket sold! 1/160

✅ 25 tickets sold
   Subject: 25 tickets sold! We're 16% full

✅ 50 tickets sold
   Subject: HALFWAY THERE! 50 tickets sold (31%)

✅ 100 tickets sold
   Subject: 100 TICKETS SOLD! Only 60 left

✅ 150 tickets sold
   Subject: ALMOST FULL! Only 10 seats remaining

✅ 160 tickets sold (FULL)
   Subject: SOLD OUT! All seats taken!
```

---

## 🎯 Real Data Requirements

### **Rule #1: ONLY Update from Donorbox**
```
✓ Check Donorbox dashboard
✓ Use that number
✓ Update Admin Panel
✓ Done

✗ Don't guess
✗ Don't use old numbers
✗ Don't estimate
✗ Don't use "last I remember"
```

### **Rule #2: Update Daily**
```
✓ Every day at 3 PM
✓ Takes 5 minutes
✓ Keeps data current
✓ Website always accurate

✗ Don't skip days
✗ Don't update weekly
✗ Don't batch updates
✗ Don't forget
```

### **Rule #3: Verify Before & After**
```
BEFORE:
├─ Check Donorbox count
└─ Write it down

AFTER:
├─ Check website shows it
├─ Check Admin Panel saved
└─ Check tracking spreadsheet updated
```

---

## 📋 Tracking Spreadsheet Template

**Create in Google Sheets:**

```
Columns:
A: Date
B: Day of Week
C: Donorbox Check Time
D: Tickets Sold (from Donorbox)
E: Previous Count (verify no decrease)
F: Seats Remaining (160 - sold)
G: Capacity % ([sold/160]*100)
H: Updated in Admin Panel? (Y/N)
I: Website Verified? (Y/N)
J: Notes
K: Team Alert Sent? (Y/N)

Sample row:
6/15/2026 | Mon | 3:00 PM | 45 | 35 | 115 | 28% | Y | Y | Growing trend | Y
```

**Share with: Michael, Dolf, Brendan, Rod**

---

## 🔄 Admin Panel Fields (Ticket Section)

### **Location:**
```
https://allhandsondecknhn.netlify.app/#admin-panel

Section: "🎟️ TICKET SALES"
```

### **Field to Update:**
```
Label: "Tickets Sold (0-160):"
Current Value: 0 (starts here)
Enter: Your actual count
Example: 127
```

### **System Calculates Automatically:**
```
Remaining = 160 - [your number]
Capacity % = ([your number] ÷ 160) × 100
Website updates instantly
No page refresh needed
```

---

## 📊 Weekly Report to Team

**Send Every Friday:**

```
SUBJECT: Weekly Ticket Sales Update

Hi Team,

TICKET SALES PROGRESS:
Current: [X] of 160 sold ([Y]%)
Previous Week: [X] of 160 sold
Increase: [+X] tickets

REMAINING: [X] seats
ON TRACK: Yes/No

TRAJECTORY:
Average per day: [X] tickets
At this rate, we'll hit 160 on: [date]

MILESTONE STATUS:
[ ] 25 tickets - ✓ Achieved
[ ] 50 tickets - ✓ Achieved
[ ] 100 tickets - In Progress
[ ] 150 tickets - Goal: Oct 15

NEXT STEPS:
├─ Social media push [date]
├─ Email campaign [date]
└─ Follow-up with leads [date]

Total Revenue (so far): $[X] ÷ $8,000 goal

Let's keep the momentum!
- Michael
```

---

## ✅ Monthly Metrics

Track and report monthly:

```
MONTH: June 2026

Total Tickets Sold: X
Average per week: X
Average per day: X
Revenue: $X

Remaining: X
Capacity Used: X%
On Target: Yes/No

Milestones Hit:
├─ [ ] 25 tickets
├─ [ ] 50 tickets
├─ [ ] 100 tickets
└─ [ ] 150 tickets

Best Selling Days: [days]
Slowest Days: [days]

Promotional Activity:
├─ Social posts: X
├─ Emails sent: X
└─ Personal contacts: X

Next Month Target: [X] tickets
```

---

## 🎯 Who Updates Tickets?

**Primary:** Michael Franks (Event Chair)
```
Responsibility: Daily ticket count
Frequency: Every day at 3 PM
Contact: mpfranx@hotmail.com | 480-352-4824
```

**Backup:** Rod Dennis (Director)
```
If Michael is unavailable
Contact: rod@roddennis.com | 480-695-0733
```

**Verification:** Brendan Cassin (Treasurer)
```
Weekly reconciliation
Revenue verification
Contact: brendan.cassin@midfirst.com
```

---

## 💡 Pro Tips

### **Do:**
✓ Update every single day
✓ Always use Donorbox as source
✓ Check website immediately after
✓ Log in tracking spreadsheet
✓ Send team alerts for milestones
✓ Celebrate progress
✓ Follow up on promotional efforts

### **Don't:**
✗ Skip days
✗ Guess at numbers
✗ Use old data
✗ Forget to save in Admin Panel
✗ Ignore the spreadsheet
✗ Update only weekly
✗ Leave website showing zeros

---

## 🚀 Getting Started Today

**Right Now:**
1. ✓ Open Donorbox dashboard
2. ✓ Note current ticket count
3. ✓ Open Admin Panel
4. ✓ Update "Tickets Sold" field
5. ✓ Click Save
6. ✓ Verify website shows correct number

**From Tomorrow:**
- Same process every day at 3 PM
- Takes 5 minutes
- Keeps everything current

---

## 📞 Support

**Issues with Admin Panel?**
- Read: ADMIN_PANEL_QUICK_START.txt
- Contact: rod@roddennis.com

**Issues with Donorbox access?**
- Contact Donorbox support
- Or contact: michael@[email]

**Questions about this system?**
- Email: rod@roddennis.com
- Phone: 480-695-0733

---

## ✨ Summary

You now have a **REAL ticket tracking system** where:

✅ Numbers start at ZERO (no fake data)
✅ You enter ACTUAL sales from Donorbox
✅ Website updates automatically
✅ Tracking spreadsheet records history
✅ Team gets daily reports
✅ Transparent to all stakeholders

**Admin Panel Link:** https://allhandsondecknhn.netlify.app/#admin-panel

**Donorbox Link:** https://donorbox.org/nhn-2026-gala-tickets

**Time to update:** 5 minutes daily

**Status:** ✅ READY TO USE!

---

**Last Updated:** June 10, 2026
**Next Update:** Daily at 3 PM
**Support:** rod@roddennis.com | 480-695-0733
