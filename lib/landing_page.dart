import 'package:flutter/material.dart';
import 'login_page.dart';
import 'about_us_page.dart';

class LandingPage extends StatelessWidget {
  const LandingPage({super.key});

  // Brand color
  Color get _green => const Color(0xFF2E7D32);

  // Background color matching phone.jpg's background
  Color get _lightCreamBackground => const Color(0xFFF9F9F9); 

 // Approximate
  @override
  Widget build(BuildContext context) {
    // Responsive scaling based on width
    final width = MediaQuery.of(context).size.width;
    final scale = (width / 375).clamp(0.85, 1.25);
    double sp(double v) => v * scale;

    // Check for wide screen to adjust layout
    final isWide = width >= 720;

    return Scaffold(
      // ⭐️ CHANGE 1: Scaffold background color ⭐️
      backgroundColor: _lightCreamBackground,
      appBar: AppBar(
        backgroundColor: _lightCreamBackground, // Match app bar background
        elevation: 0,
        centerTitle: false,
        leadingWidth: sp(140),
        leading: Padding(
          padding: EdgeInsets.only(left: sp(12)),
          child: _Logo(sp: sp, green: _green),
        ),
        actions: [
          IconButton(
            iconSize: sp(24),
            icon: const Icon(Icons.menu, color: Colors.black87),
            onPressed: () => _openMenu(context),
            tooltip: 'Menu',
          ),
        ],
      ),
      body: SingleChildScrollView(
        padding: EdgeInsets.fromLTRB(sp(24), sp(16), sp(24), sp(32)),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // This LayoutBuilder makes the hero section responsive
            LayoutBuilder(
              builder: (context, constraints) {
                // Headline
                final headline = Text(
                  'Smart Farming\nStarts Here.',
                  style: Theme.of(context).textTheme.displaySmall?.copyWith(
                    fontWeight: FontWeight.w800,
                    height: 1.1,
                    color: Colors.black87,
                    fontSize: sp(36), // responsive headline
                  ),
                );

                // Sub-headline
                final subHeadline = Text(
                  'Identify crop diseases instantly with AI-powered image detection.',
                  style: Theme.of(context).textTheme.titleMedium?.copyWith(
                    color: Colors.black.withOpacity(0.7),
                    height: 1.4,
                    fontSize: sp(16),
                  ),
                );

                // Download Button
                final downloadButton = SizedBox(
                  height: sp(48),
                  child: ElevatedButton(
                    onPressed: () {
                      Navigator.push(
                        context,
                        MaterialPageRoute(builder: (_) => const LoginPage()),
                      );
                    },
                    style: ElevatedButton.styleFrom(
                      elevation: 0,
                      backgroundColor: _green,
                      foregroundColor: Colors.white,
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(sp(10)),
                      ),
                      padding: EdgeInsets.symmetric(horizontal: sp(24)),
                    ),
                    child: Text(
                      'Download AgriCheck',
                      style: TextStyle(
                        fontWeight: FontWeight.w700,
                        fontSize: sp(15),
                      ),
                    ),
                  ),
                );

                final heroArt = _HeroArt(sp: sp);

                // ⭐️ CHANGE 2: Layout for Hero Section ⭐️
                // This adjusts the placement of the button relative to the image
                if (isWide) {
                  return Column(
                    // Keep headline at the top
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      headline,
                      SizedBox(height: sp(16)),
                      Row(
                        // Place sub-headline/button and image side-by-side
                        crossAxisAlignment: CrossAxisAlignment.center,
                        children: [
                          Expanded(
                            flex: 2,
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                subHeadline,
                                SizedBox(height: sp(24)),
                                downloadButton,
                              ],
                            ),
                          ),
                          SizedBox(width: sp(32)),
                          Expanded(
                            flex: 3,
                            child: heroArt, // The image
                          ),
                        ],
                      ),
                    ],
                  );
                }

                // Stacked on mobile screens (original layout, adjusted slightly)
                return Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    headline,
                    SizedBox(height: sp(16)),
                    subHeadline,
                    SizedBox(height: sp(24)),
                    downloadButton,
                    SizedBox(height: sp(32)),
                    Center(child: heroArt), // Center image on mobile
                  ],
                );
              },
            ),

            SizedBox(height: sp(40)),

            // --- Features Section ---
            Text(
              'Features',
              style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                fontWeight: FontWeight.w700,
                color: Colors.black87,
                fontSize: sp(22),
              ),
            ),
            SizedBox(height: sp(24)),
            _FeatureItem(
              sp: sp,
              green: _green,
              icon: Icons.local_florist_outlined,
              title: 'Disease Detection',
            ),
            SizedBox(height: sp(20)),
            _FeatureItem(
              sp: sp,
              green: _green,
              icon: Icons.camera_alt_outlined,
              title: 'Image-based Scanning',
            ),
            SizedBox(height: sp(20)),
            _FeatureItem(
              sp: sp,
              green: _green,
              icon: Icons.bar_chart_rounded,
              title: 'Real-time Reports',
            ),
          ],
        ),
      ),
    );
  }

  // --- Widgets ---
  void _openMenu(BuildContext context) {
    showModalBottomSheet(
      context: context,
      showDragHandle: true,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(16)),
      ),
      builder: (ctx) => Padding(
        padding: const EdgeInsets.fromLTRB(16, 8, 16, 24),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            _NavBtn(
              label: 'Login',
              icon: Icons.login,
              onTap: () => _go(ctx, const LoginPage()),
            ),
            _NavBtn(
              label: 'About Us',
              icon: Icons.info_outline,
              onTap: () => _go(ctx, const AboutUsPage()),
            ),
          ],
        ),
      ),
    );
  }

  void _go(BuildContext ctx, Widget page) {
    Navigator.pop(ctx);
    Navigator.of(ctx).push(MaterialPageRoute(builder: (_) => page));
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

/// Left side: headline + subcopy + CTA (responsive)
// Removed the content from here as it's now handled in the parent LayoutBuilder
class _HeroCopy extends StatefulWidget {
  final double Function(double) sp;
  final Color green;

  const _HeroCopy({required this.sp, required this.green});

  @override
  State<_HeroCopy> createState() => _HeroCopyState();
}

class _HeroCopyState extends State<_HeroCopy> {
  @override
  Widget build(BuildContext context) {
    // This widget is now primarily a placeholder as its content is managed
    // directly in the LandingPage's LayoutBuilder to allow for flexible
    // positioning with the image.
    return const SizedBox.shrink(); // Return an empty widget
  }
}

/// Right side: The hero illustration
class _HeroArt extends StatelessWidget {
  final double Function(double) sp;
  const _HeroArt({required this.sp});

  @override
  Widget build(BuildContext context) {
    return Container(
      height: sp(220),
      alignment: Alignment.center,
      child: Image.asset('assets/images/phone.jpg', fit: BoxFit.contain),
    );
  }
}

/// A single feature item (Icon + Text)
class _FeatureItem extends StatelessWidget {
  final IconData icon;
  final String title;
  final double Function(double) sp;
  final Color green;

  const _FeatureItem({
    required this.icon,
    required this.title,
    required this.sp,
    required this.green,
  });

  @override
  Widget build(BuildContext context) {
    return Row(
      crossAxisAlignment: CrossAxisAlignment.center,
      children: [
        Icon(icon, color: green, size: sp(28)),
        SizedBox(width: sp(16)),
        Expanded(
          child: Text(
            title,
            style: TextStyle(
              fontSize: sp(16),
              fontWeight: FontWeight.w600,
              color: Colors.black87,
            ),
          ),
        ),
      ],
    );
  }
}

/// Navigation button for the modal menu
class _NavBtn extends StatelessWidget {
  final String label;
  final IconData icon;
  final VoidCallback onTap;
  const _NavBtn({required this.label, required this.icon, required this.onTap});

  @override
  Widget build(BuildContext context) {
    return ListTile(
      contentPadding: const EdgeInsets.symmetric(horizontal: 6),
      leading: Icon(icon),
      title: Text(label, style: const TextStyle(fontWeight: FontWeight.w600)),
      onTap: onTap,
      trailing: const Icon(Icons.chevron_right),
    );
  }
}
