import 'package:flutter/material.dart';
import 'login_page.dart';
import 'about_us_page.dart';
import 'home_page.dart';
import 'edit_profile_page.dart';
import 'scan_history_page.dart';
import 'help_page.dart';

class ProfilePage extends StatelessWidget {
  const ProfilePage({super.key});

  // Colors from your theme
  Color get _green => const Color(0xFF1B5E20); // Dark Green
  Color get _bgColor => Colors.grey.shade50;

  // --- Logout Function ---
  void _logout(BuildContext context) {
    Navigator.pushAndRemoveUntil(
      context,
      MaterialPageRoute(builder: (_) => const LoginPage()),
      (route) => false, // Clear all routes
    );
  }

  @override
  Widget build(BuildContext context) {
    // Responsive scaling
    final width = MediaQuery.of(context).size.width;
    final scale = (width / 375).clamp(0.85, 1.25);
    double sp(double v) => v * scale;

    return Scaffold(
      backgroundColor: _bgColor,

      // --- 2. ADDED THE APP BAR ---
      appBar: AppBar(
        backgroundColor: _bgColor,
        elevation: 0,
        foregroundColor: Colors.black87,
        title: Text(
          'Profile & Settings',
          style: TextStyle(fontSize: sp(18), fontWeight: FontWeight.w600),
        ),
        // --- 3. ADDED THE BACK BUTTON ---
        leading: IconButton(
          icon: const Icon(Icons.arrow_back_ios_new_rounded),
          iconSize: sp(20),
          onPressed: () {
            // This will navigate back to a new instance of the HomePage.
            // This is used instead of pop() because this page is a main tab.
            Navigator.pushAndRemoveUntil(
              context,
              MaterialPageRoute(builder: (_) => const HomePage()),
              (route) => false,
            );
          },
        ),
      ),
      body: SingleChildScrollView(
        padding: EdgeInsets.all(sp(16)),
        child: Column(
          children: [
            // --- User Info ---
            _buildProfileHeader(sp: sp),
            SizedBox(height: sp(32)),

            // --- Menu List ---
            _buildSettingsList(context, sp: sp),
            SizedBox(height: sp(40)),

            // --- Logout Button ---
            SizedBox(
              width: double.infinity,
              height: sp(50),
              child: ElevatedButton(
                onPressed: () => _logout(context),
                style: ElevatedButton.styleFrom(
                  backgroundColor: _green,
                  foregroundColor: Colors.white,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(sp(10)),
                  ),
                ),
                child: Text(
                  'Log Out',
                  style: TextStyle(
                    fontSize: sp(16),
                    fontWeight: FontWeight.w600,
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  // --- Profile Header Widget ---
  Widget _buildProfileHeader({required double Function(double) sp}) {
    return Column(
      children: [
        CircleAvatar(
          radius: sp(40),
          backgroundColor: _green.withOpacity(0.1),
          child: Icon(Icons.person, size: sp(45), color: _green),
        ),
        SizedBox(height: sp(12)),
        Text(
          'Farmer Juan', // Mock data
          style: TextStyle(
            fontSize: sp(22),
            fontWeight: FontWeight.w700,
            color: Colors.black87,
          ),
        ),
        SizedBox(height: sp(4)),
        Text(
          'juan@farmer.com', // Mock data
          style: TextStyle(fontSize: sp(15), color: Colors.grey.shade600),
        ),
      ],
    );
  }

  // --- Settings List Widget ---
  Widget _buildSettingsList(
    BuildContext context, {
    required double Function(double) sp,
  }) {
    return Container(
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(sp(12)),
        border: Border.all(color: Colors.grey.shade200),
      ),
      child: Column(
        children: [
          _SettingsTile(
            sp: sp,
            icon: Icons.person_outline,
            title: 'Edit Profile',
            onTap: () {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (_) => const EditProfilePage()),
              );
            },
          ),
          _SettingsTile(
            sp: sp,
            icon: Icons.history_rounded,
            title: 'Scan History',
            onTap: () {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (_) => const ScanHistoryPage()),
              );
            },
          ),
          _SettingsTile(
            sp: sp,
            icon: Icons.info_outline_rounded,
            title: 'About Us',
            onTap: () {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (_) => const AboutUsPage()),
              );
            },
          ),
          _SettingsTile(
            sp: sp,
            icon: Icons.help_outline_rounded,
            title: 'Help & Support',
            isLast: true,
            onTap: () {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (_) => const HelpPage()),
              );
            },
          ),
        ],
      ),
    );
  }
}

// --- Reusable ListTile for Settings ---
class _SettingsTile extends StatelessWidget {
  final double Function(double) sp;
  final IconData icon;
  final String title;
  final VoidCallback onTap;
  final bool isLast;

  const _SettingsTile({
    required this.sp,
    required this.icon,
    required this.title,
    required this.onTap,
    this.isLast = false,
  });

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: onTap,
      child: Container(
        padding: EdgeInsets.symmetric(horizontal: sp(16), vertical: sp(14)),
        decoration: BoxDecoration(
          border: isLast
              ? null
              : Border(
                  bottom: BorderSide(color: Colors.grey.shade200, width: 1),
                ),
        ),
        child: Row(
          children: [
            Icon(icon, color: Colors.grey.shade700, size: sp(22)),
            SizedBox(width: sp(16)),
            Expanded(
              child: Text(
                title,
                style: TextStyle(
                  fontSize: sp(15),
                  fontWeight: FontWeight.w500,
                  color: Colors.black87,
                ),
              ),
            ),
            Icon(
              Icons.chevron_right_rounded,
              color: Colors.grey.shade500,
              size: sp(22),
            ),
          ],
        ),
      ),
    );
  }
}
