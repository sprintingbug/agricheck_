import 'package:flutter/material.dart';
import 'scan_page.dart';
import 'profile_page.dart';
import 'login_page.dart';
import 'weather_page.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  // 0 = Home, 1 = Settings. Scan is the FAB.
  int _currentIndex = 0;

  Color get _green => const Color(0xFF1B5E20); // Dark Green
  Color get _lightGreen => const Color(0xFF388E3C); // Medium Green
  // ignore: unused_element
  Color get _accentGreen => const Color(0xFFA5D6A7); // Lightest Green
  Color get _bgColor => Colors.grey.shade50;

  // This will hold the different pages/screens
  final List<Widget> _pages = [
    const _HomePageContent(), // Tab 0: Home
    const ProfilePage(), // Tab 1: Settings
  ];

  void _onTabTapped(int index) {
    if (index == 2) {
      // "Log Out" is now an action, not a tab
      _logout(context);
    } else {
      setState(() => _currentIndex = index);
    }
  }

  void _scan() {
    Navigator.push(
      context,
      MaterialPageRoute(builder: (_) => const ScanPage()),
    );
  }

  void _logout(BuildContext context) {
    Navigator.pushAndRemoveUntil(
      context,
      MaterialPageRoute(builder: (_) => const LoginPage()),
      (route) => false,
    );
  }

  @override
  Widget build(BuildContext context) {
    final size = MediaQuery.of(context).size;
    final width = size.width;
    final scale = (width / 375).clamp(0.85, 1.25);
    double sp(double v) => v * scale;
    final paddingSafeTop = MediaQuery.of(context).padding.top;

    return Scaffold(
      backgroundColor: _bgColor,
      // --- Custom AppBar ---
      appBar: PreferredSize(
        preferredSize: Size.fromHeight(sp(60) + paddingSafeTop),
        child: SafeArea(
          bottom: false,
          child: Padding(
            padding: EdgeInsets.symmetric(horizontal: sp(16), vertical: sp(8)),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                // Logo
                _Logo(sp: sp, green: _green),
                // Profile Icon
                GestureDetector(
                  onTap: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(builder: (_) => const ProfilePage()),
                    );
                  },
                  child: CircleAvatar(
                    backgroundColor: _lightGreen.withOpacity(0.15),
                    radius: sp(20),
                    child: Icon(Icons.person, color: _lightGreen, size: sp(24)),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),

      // --- Body ---
      // Use IndexedStack to keep state of pages when switching tabs
      body: IndexedStack(index: _currentIndex, children: _pages),

      // --- Floating Action Button (Scan) ---
      floatingActionButton: SizedBox(
        height: sp(64),
        width: sp(64),
        child: FittedBox(
          child: FloatingActionButton(
            onPressed: _scan,
            backgroundColor: _lightGreen,
            foregroundColor: Colors.white,
            elevation: 2,
            child: Icon(Icons.document_scanner_outlined, size: sp(28)),
          ),
        ),
      ),
      floatingActionButtonLocation: FloatingActionButtonLocation.centerDocked,

      // --- Bottom Navigation Bar ---
      bottomNavigationBar: BottomAppBar(
        color: _green,
        height: sp(60),
        shape: const CircularNotchedRectangle(), // Creates the "dock"
        notchMargin: 8.0,
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceAround,
          children: [
            _buildNavItem(
              icon: Icons.home_rounded,
              label: 'Home',
              index: 0,
              sp: sp,
            ),
            // This is a spacer for the FAB
            SizedBox(width: sp(40)),
            _buildNavItem(
              icon: Icons.settings_rounded,
              label: 'Settings',
              index: 1,
              sp: sp,
            ),
          ],
        ),
      ),
    );
  }

  // Helper widget for a single navigation bar item
  Widget _buildNavItem({
    required IconData icon,
    required String label,
    required int index,
    required double Function(double) sp,
  }) {
    final isSelected = _currentIndex == index;
    return Expanded(
      child: InkWell(
        onTap: () => _onTabTapped(index),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(
              icon,
              size: sp(24),
              color: isSelected ? Colors.white : Colors.white.withOpacity(0.7),
            ),
            SizedBox(height: sp(4)),
            Text(
              label,
              style: TextStyle(
                fontSize: sp(12),
                color: isSelected
                    ? Colors.white
                    : Colors.white.withOpacity(0.7),
                fontWeight: isSelected ? FontWeight.w600 : FontWeight.w500,
              ),
            ),
          ],
        ),
      ),
    );
  }
}

/// --- Main Home Page Content ---
/// (This is separated to work with the IndexedStack)
class _HomePageContent extends StatelessWidget {
  const _HomePageContent();

  @override
  Widget build(BuildContext context) {
    // ⭐️ Get MediaQuery width here
    final size = MediaQuery.of(context).size;
    final width = size.width;
    final scale = (width / 375).clamp(0.85, 1.25);
    double sp(double v) => v * scale;

    return SingleChildScrollView(
      padding: EdgeInsets.all(sp(16)),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // --- Greeting ---
          Text(
            'Hello, Farmer Juan 👋',
            style: TextStyle(
              fontSize: sp(24),
              fontWeight: FontWeight.w800,
              color: Colors.black87,
            ),
          ),
          SizedBox(height: sp(24)),

          // --- Hero Section (Scan + Farmer) ---
          // ⭐️ Pass the screen width to the hero builder
          _buildHeroSection(context, sp, width),

          SizedBox(height: sp(32)),

          // --- Quick Stats ---
          Text(
            'Quick Stats',
            style: TextStyle(
              fontSize: sp(20),
              fontWeight: FontWeight.w700,
              color: Colors.black87,
            ),
          ),
          SizedBox(height: sp(16)),

          GridView.count(
            crossAxisCount: 2,
            crossAxisSpacing: sp(12),
            mainAxisSpacing: sp(12),
            shrinkWrap: true,
            physics: const NeverScrollableScrollPhysics(),
            childAspectRatio: 1.1, // Adjusted aspect ratio
            children: [
              _StatCard(
                icon: Icons.grass_rounded, // Matches "wheat" icon better
                title: 'Healthy Crops',
                color: const Color(0xFFE6F4EA),
                sp: sp,
              ),
              _StatCard(
                icon: Icons.warning_amber_rounded,
                title: 'Diseases',
                color: const Color(0xFFE6F4EA),
                sp: sp,
              ),
              _StatCard(
                icon: Icons.bar_chart_rounded, // Matches "reports" icon
                title: 'Reports',
                color: const Color(0xFFE6F4EA),
                sp: sp,
              ),
              _StatCard(
                icon: Icons.wb_sunny_outlined,
                title: 'Weather',
                color: const Color(0xFFE6F4EA),
                sp: sp,
                onTap: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(builder: (_) => const WeatherPage()),
                  );
                },
              ),
            ],
          ),
        ],
      ),
    );
  }

  // --- Hero Section Widget ---
  // ⭐️ Changed LayoutBuilder to use the 'screenWidth' parameter
  Widget _buildHeroSection(
    BuildContext context,
    double Function(double) sp,
    double screenWidth, // Now accepts screen width
  ) {
    Color green = const Color(0xFF388E3C);

    // This is the content for the "Scan" side
    final scanContent = Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        GestureDetector(
          onTap: () {
            Navigator.push(
              context,
              MaterialPageRoute(builder: (_) => const ScanPage()),
            );
          },
          child: Container(
            padding: EdgeInsets.all(sp(12)),
            decoration: BoxDecoration(
              color: green.withOpacity(0.1),
              borderRadius: BorderRadius.circular(sp(16)),
            ),
            child: Column(
              children: [
                Icon(Icons.camera_alt_rounded, size: sp(80), color: green),
                SizedBox(height: sp(8)),
                Container(
                  padding: EdgeInsets.symmetric(
                    horizontal: sp(10),
                    vertical: sp(4),
                  ),
                  decoration: BoxDecoration(
                    color: green,
                    borderRadius: BorderRadius.circular(sp(6)),
                  ),
                  child: Text(
                    'Scan Plant for Disease',
                    style: TextStyle(
                      color: Colors.white,
                      fontWeight: FontWeight.w600,
                      fontSize: sp(11),
                    ),
                  ),
                ),
              ],
            ),
          ),
        ),
        SizedBox(height: sp(8)),
        Text(
          'Tap to take a photo and get instant results.',
          style: TextStyle(fontSize: sp(12), color: Colors.black54),
        ),
      ],
    );

    // This is the farmer image
    final farmerArt = _FarmerArt(sp: sp);

    // ⭐️ Check if the screen is very narrow using 'screenWidth'
    if (screenWidth < 360) {
      // If so, stack them in a Column
      return Column(
        children: [
          scanContent,
          SizedBox(height: sp(16)),
          farmerArt,
        ],
      );
    }

    // Otherwise, use the original Row layout
    return Row(
      children: [
        Expanded(flex: 3, child: scanContent),
        SizedBox(width: sp(16)),
        Expanded(flex: 4, child: farmerArt),
      ],
    );
  }
}

// --- Reusable Widgets ---

/// Farmer Illustration
class _FarmerArt extends StatelessWidget {
  final double Function(double) sp;
  const _FarmerArt({required this.sp});

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      height: sp(200), // Increased height for the image (was 180)
      child: Align(
        // Use Align to center the image if it's smaller than SizedBox
        alignment: Alignment.bottomCenter, // Align to bottom if needed
        child: Image.asset(
          'assets/images/hiworain.jpg',
          fit: BoxFit.contain,
          height: sp(200), // Specify height for the image itself
        ),
      ),
    );
  }
}

/// AGRICHECK wordmark (responsive)
class _Logo extends StatelessWidget {
  final double Function(double) sp;
  final Color green;

  const _Logo({required this.sp, required this.green});

  @override
  Widget build(BuildContext context) {
    return Container(
      alignment: Alignment.centerLeft,
      child: DecoratedBox(
        decoration: BoxDecoration(
          color: const Color(0xFFE8F5E9),
          borderRadius: BorderRadius.circular(sp(8)),
          border: Border.all(color: const Color(0xFF1B5E20), width: 2),
        ),
        child: Padding(
          padding: EdgeInsets.symmetric(horizontal: sp(10), vertical: sp(6)),
          child: Text(
            'AGRICHECK',
            style: TextStyle(
              fontSize: sp(16),
              letterSpacing: 1.1,
              fontWeight: FontWeight.w900,
              color: green,
            ),
          ),
        ),
      ),
    );
  }
}

/// Stat Card for the Grid
class _StatCard extends StatelessWidget {
  final IconData icon;
  final String title;
  final Color color;
  final VoidCallback? onTap;
  final double Function(double) sp;

  const _StatCard({
    required this.icon,
    required this.title,
    required this.color,
    required this.sp,
    this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return InkWell(
      borderRadius: BorderRadius.circular(sp(16)),
      onTap: onTap,
      child: Container(
        decoration: BoxDecoration(
          color: color,
          borderRadius: BorderRadius.circular(sp(16)),
        ),
        child: Center(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Icon(icon, size: sp(36), color: Colors.black87),
              SizedBox(height: sp(12)),
              Text(
                title,
                textAlign: TextAlign.center,
                style: TextStyle(
                  fontSize: sp(15),
                  fontWeight: FontWeight.w600,
                  color: Colors.black,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
