# Admin Panel Guide - Live Data Management

## 🎯 Overview

The Admin Panel is a **hidden control center** on your website where event coordinators can update real numbers. Instead of hardcoding fake data, all numbers are:
- Entered in the Admin Panel
- Saved to browser storage
- Displayed live on the website
- Updated instantly with no code changes needed

---

## 🔐 Accessing the Admin Panel

### Method 1: Direct Link
Add `#admin-panel` to your website URL:
```
https://allhandsondecknhn.netlify.app/#admin-panel
```

### Method 2: From Website Footer
1. Scroll to bottom of website
2. Look for "Accessibility" section
3. Click the blue "Admin Panel" link

### Method 3: JavaScript Command
In browser console, type:
```javascript
toggleAdminPanel()
```

---

## 📊 What You Can Update

The Admin Panel has 5 sections:

### 1️⃣ **Ticket Sales**
```
Field: Tickets Sold (0-160)
Updates: 
├─ Homepage ticket counter
├─ "X of 160 sold" display
├─ Capacity percentage
└─ Remaining seats count
```

### 2️⃣ **Sponsorships**
```
Fields: 
├─ Sponsorship Tiers Committed (number)
└─ Total Sponsorship Revenue (dollars)

Updates:
├─ "X tiers committed" display
└─ Total sponsorship revenue shown
```

### 3️⃣ **Revenue Breakdown**
```
Fields:
├─ Tickets Total Revenue ($)
├─ Live Auction Revenue ($)
├─ Silent Auction Revenue ($)
├─ 50/50 Raffle Revenue ($)
└─ Paddle Raise Revenue ($)

Updates:
└─ Total Revenue = Sum of all above
```

### 4️⃣ **Live Preview**
Shows you exactly what visitors will see:
```
Tickets: 127 / 160
Sponsors: 13 tiers
Total Revenue: $31,725
Last updated: [timestamp]
```

### 5️⃣ **Action Buttons**
```
💾 Save & Update Live Site
  → Saves all data
  → Updates website
  → Shows confirmation

Close Panel
  → Hides the admin panel
```

---

## 🚀 How to Use (Step-by-Step)

### Step 1: Access the Admin Panel
Go to: `https://allhandsondecknhn.netlify.app/#admin-panel`

### Step 2: Get Current Numbers
**From your tracking spreadsheet:**
- Tickets Sold: Count from Attendee_Tracking.csv
- Sponsorships: Count from sponsorship commitments
- Revenue: Sum all revenue sources

### Step 3: Enter Numbers
1. **Tickets Sold:** Enter actual count (example: 127)
2. **Sponsorship Tiers:** Enter number committed (example: 13)
3. **Sponsorship Revenue:** Enter total $ (example: 25375)
4. **Revenue Breakdown:**
   - Tickets: 127 × $50 = 6350
   - Live Auction: (sum of items sold)
   - Silent Auction: (sum of items sold)
   - 50/50 Raffle: (tickets sold × $20)
   - Paddle Raise: (donations received)

### Step 4: Review Preview
Check the "Live Preview" box to see exactly what visitors will see

### Step 5: Save & Update
Click **"💾 Save & Update Live Site"**

### Step 6: Confirmation
You'll see a popup showing:
```
✅ Data saved and updated!

Tickets: 127/160
Sponsors: 13 tiers
Revenue: $31,725

Website will update automatically!
```

### Step 7: Close Panel
Click **"Close Panel"** or navigate away

---

## 📱 What Changes on Website

After you save, these automatically update:

### Homepage Display
```
TICKETS SOLD
127
of 160 capacity (79.4%)

SPONSORSHIPS SECURED
13
tiers committed

REVENUE TO DATE
$31.7K
of $45K goal
```

### Sponsorship Section
```
Ticket Availability
✓ 127 of 160 tickets sold
✓ Only 33 seats remaining
✓ 79% capacity
```

### All Counters Update Automatically
- No page refresh needed
- Changes appear instantly
- Works on mobile & desktop

---

## 🔄 Daily Update Routine

### Every Day at 3 PM (example schedule)
1. Open tracking spreadsheet
2. Check new registrations
3. Access Admin Panel
4. Update ticket count
5. Update revenue totals
6. Click Save
7. Confirm on website

### Weekly Summary (Every Friday)
1. Calculate weekly totals
2. Update sponsorship tier count
3. Add any auction/raffle income
4. Save to Admin Panel
5. Send update email to team

---

## 💾 Data Storage & Backup

### How Data is Saved
- **Storage:** Browser's localStorage
- **Device:** Saved on the computer used
- **Persistence:** Data stays even if you close browser
- **Backup:** Create `data.json` backup monthly

### How to Backup Data

#### Manual Backup
1. Open Admin Panel
2. Copy all numbers
3. Paste into spreadsheet (Excel/Google Sheets)
4. Save with timestamp

#### Automated Backup (Monthly)
```
Create a backup folder:
C:\Users\rodde\OneDrive\Documentos\AllHandsOnDeck\backups

Save as: data_backup_[DATE].json
Example: data_backup_2026-06-10.json
```

### Important ⚠️
- **Use SAME computer** for updates (data is device-specific)
- If using different computer, manually re-enter numbers
- OR share Admin Panel link & each person updates from their device

---

## 👥 Team Sharing Instructions

### For Michael Franks (Event Chair)
**Send him:**
1. Website URL: `https://allhandsondecknhn.netlify.app/#admin-panel`
2. Instructions: Use steps in "How to Use"
3. Backup file: `data.json`

**Tell him:**
- Only update from same computer
- Click "Save & Update Live Site" after each change
- Website updates automatically

### For Rod Dennis (Director)
**Send him:**
1. Admin Panel link
2. This guide (ADMIN_PANEL_GUIDE.md)
3. Monthly backup spreadsheet

### For Dolf May (Sponsorship Chair)
**Send him:**
1. Admin Panel link
2. Instructions for updating sponsorship numbers
3. Weekly revenue update procedure

### For Brendan Cassin (Treasurer)
**Send him:**
1. Admin Panel link
2. Revenue breakdown instructions
3. Monthly reconciliation checklist

---

## 🔧 Troubleshooting

### Problem: Admin Panel won't open
**Solution:**
- Refresh page
- Try clicking Admin Panel link again
- Check browser console for errors

### Problem: Changes not saving
**Solution:**
- Make sure to click "💾 Save & Update Live Site"
- Check browser localStorage is enabled
- Try closing & reopening browser

### Problem: Numbers don't match website
**Solution:**
- Refresh website page
- Check browser cache (clear if needed)
- Verify numbers in Admin Panel match

### Problem: Can't access from different computer
**Solution:**
- Data is stored per computer
- Re-enter numbers on new computer
- OR use shared spreadsheet + 1 coordinator per device

### Problem: Data disappeared
**Solution:**
- Check browser history restoration
- Look in `data_backup_*.json` files
- Restore from backup spreadsheet

---

## 📋 Update Checklist

**Daily:**
- [ ] Check new ticket sales
- [ ] Update "Tickets Sold" number
- [ ] Click Save

**Weekly:**
- [ ] Count sponsorship tiers
- [ ] Update sponsorship revenue
- [ ] Calculate auction/raffle income
- [ ] Update revenue fields
- [ ] Click Save
- [ ] Email team update

**Monthly:**
- [ ] Review all numbers
- [ ] Create data backup
- [ ] Reconcile with spreadsheet
- [ ] Send financial report

---

## 📞 Support

**Questions about Admin Panel?**
- Email: rod@roddennis.com
- Phone: 480-695-0733

**Technical issues?**
- Check browser console (F12)
- Try clearing browser cache
- Ensure JavaScript is enabled

---

## 🎓 Advanced Tips

### Create Dashboard Bookmark
1. Open Admin Panel
2. Bookmark the page (Ctrl+D)
3. Name it: "AHOD Admin"
4. Access daily from bookmark

### Use Spreadsheet Formula
Create a formula in Google Sheets that reminds you to update:
```
=IF(TODAY()=DATE(2026,6,10),"UPDATE ADMIN PANEL!","")
```

### Set Phone Reminder
Set daily reminder on phone:
- Time: 3 PM daily
- Message: "Update AHOD Admin Panel"
- Link: `https://allhandsondecknhn.netlify.app/#admin-panel`

### Schedule Team Updates
**Weekly Zoom Call (Every Friday 4 PM):**
- Michael reviews ticket sales
- Dolf reviews sponsorships
- Brendan reviews finances
- Rod updates Admin Panel live
- Share updated numbers in email

---

## 🎯 Key Points to Remember

✅ **DO:**
- Use SAME computer for updates
- Click "Save & Update Live Site" after each change
- Update daily if possible
- Create monthly backups
- Share this guide with team

❌ **DON'T:**
- Hardcode numbers in HTML
- Edit source code to change numbers
- Use different computers without backup
- Forget to save changes
- Share Admin Panel password (it's not password protected yet - use URL sharing only)

---

## 📊 Example Update Workflow

```
MONDAY 3 PM:
1. Open Admin Panel: https://allhandsondecknhn.netlify.app/#admin-panel
2. Check spreadsheet:
   - Tickets Sold: 127
   - Sponsors: 13
   - Revenue: $31,725
3. Update Admin Panel fields
4. Review Live Preview
5. Click Save
6. See confirmation: ✅ Data saved!
7. Email team: "Updated to 127 tickets, $31.7K revenue"

FRIDAY 4 PM:
1. Weekly review meeting (via Zoom)
2. Michael: "We gained 5 tickets (127 → 132)"
3. Dolf: "Two new sponsors (13 → 15), +$3,500"
4. Brendan: "Total revenue now $35,225"
5. Rod updates Admin Panel with new numbers
6. Everyone sees updated website

MONTH END:
1. Create backup: data_backup_2026-06-30.json
2. Spreadsheet reconciliation
3. Financial summary report
4. Archive numbers for next month
```

---

## 🚀 What's Next?

After setting up Admin Panel:
1. ✅ Share link with all coordinators
2. ✅ Provide this guide to team
3. ✅ Establish daily update routine
4. ✅ Set weekly review meetings
5. ✅ Create monthly backup procedure
6. ✅ Monitor for accuracy

---

**Last Updated:** June 10, 2026
**Status:** ✅ Ready to Use
**Support:** rod@roddennis.com | 480-695-0733
