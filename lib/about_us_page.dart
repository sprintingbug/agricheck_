import 'package:flutter/material.dart';

class AboutUsPage extends StatelessWidget {
  const AboutUsPage({super.key});

  // Colors from your theme
  Color get _green => const Color(0xFF1B5E20); // Dark Green
  Color get _lightGreen => const Color(0xFF388E3C); // Medium Green
  Color get _bgColor => Colors.grey.shade50;

  @override
  Widget build(BuildContext context) {
    // Responsive scaling
    final width = MediaQuery.of(context).size.width;
    final scale = (width / 375).clamp(0.85, 1.25);
    double sp(double v) => v * scale;

    return Scaffold(
      backgroundColor: _bgColor,
      appBar: AppBar(
        title: const Text('About Us'),
        backgroundColor: _bgColor,
        foregroundColor: Colors.black87,
        elevation: 0,
      ),
      body: SingleChildScrollView(
        padding: EdgeInsets.all(sp(16)),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // --- Header Card ---
            Container(
              width: double.infinity,
              padding: EdgeInsets.all(sp(20)),
              decoration: BoxDecoration(
                color: _green,
                borderRadius: BorderRadius.circular(sp(16)),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Icon(Icons.eco_rounded, color: Colors.white, size: sp(40)),
                  SizedBox(height: sp(12)),
                  Text(
                    'AgriCheck',
                    style: TextStyle(
                      fontSize: sp(28),
                      fontWeight: FontWeight.w800,
                      color: Colors.white,
                      letterSpacing: 0.2,
                    ),
                  ),
                  SizedBox(height: sp(4)),
                  Text(
                    'Smart Crop Disease Identifier',
                    style: TextStyle(
                      fontSize: sp(16),
                      color: Colors.white.withOpacity(0.9),
                    ),
                  ),
                ],
              ),
            ),
            SizedBox(height: sp(24)),

            // --- Mission Statement ---
            _buildSectionTitle(sp: sp, title: 'Our Mission'),
            SizedBox(height: sp(8)),
            Text(
              'AgriCheck helps farmers identify crop diseases using AI-powered image detection. '
              'Scan plants, view instant results, and track insights to keep your crops healthy.',
              style: TextStyle(
                fontSize: sp(15),
                height: 1.5,
                color: Colors.black87,
              ),
            ),
            SizedBox(height: sp(24)),

            // --- How It Works ---
            _buildSectionTitle(sp: sp, title: 'How It Works'),
            SizedBox(height: sp(12)),
            _buildStep(
              sp: sp,
              icon: Icons.camera_alt_outlined,
              text:
                  'Snap a photo of the plant leaf using your phone\'s camera.',
            ),
            SizedBox(height: sp(12)),
            _buildStep(
              sp: sp,
              icon: Icons.analytics_outlined,
              text:
                  'Our AI model analyzes the image to identify potential diseases.',
            ),
            SizedBox(height: sp(12)),
            _buildStep(
              sp: sp,
              icon: Icons.article_outlined,
              text: 'Receive instant results and actionable recommendations.',
            ),
          ],
        ),
      ),
    );
  }

  // Helper for section titles
  Widget _buildSectionTitle({
    required double Function(double) sp,
    required String title,
  }) {
    return Text(
      title,
      style: TextStyle(
        fontSize: sp(18),
        fontWeight: FontWeight.w700,
        color: _green,
      ),
    );
  }

  // Helper for "How it works" steps
  Widget _buildStep({
    required double Function(double) sp,
    required IconData icon,
    required String text,
  }) {
    return Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Icon(icon, size: sp(22), color: _lightGreen),
        SizedBox(width: sp(12)),
        Expanded(
          child: Text(
            text,
            style: TextStyle(
              fontSize: sp(15),
              height: 1.4,
              color: Colors.black87,
            ),
          ),
        ),
      ],
    );
  }
}
