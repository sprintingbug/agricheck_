import 'dart:async'; // Make sure this is imported
import 'package:flutter/material.dart';
import 'landing_page.dart'; // This is where it will go after

class SplashPage extends StatefulWidget {
  const SplashPage({super.key});

  @override
  State<SplashPage> createState() => _SplashPageState();
}

class _SplashPageState extends State<SplashPage>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _scaleAnimation;

  @override
  void initState() {
    super.initState();

    // 1. Set up the Animation Controller
    _controller = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 1500),
    );

    // 2. Create the "zoom-in" animation
    _scaleAnimation = CurvedAnimation(
      parent: _controller,
      curve: Curves.easeOutBack, // This curve gives a nice "bounce"
    );

    // 3. Start the animation
    _controller.forward();

    // 4. Set a timer to navigate to the LandingPage
    Timer(const Duration(seconds: 3), _navigateToLandingPage);
  }

  void _navigateToLandingPage() {
    if (!mounted) return; // Check if the widget is still on screen

    // Use pushReplacement so the user can't press "back" to the splash screen
    Navigator.pushReplacement(
      context,
      // Use PageRouteBuilder for a smooth fade-in transition
      PageRouteBuilder(
        pageBuilder: (context, animation, secondaryAnimation) =>
            const LandingPage(),
        transitionsBuilder: (context, animation, secondaryAnimation, child) {
          return FadeTransition(opacity: animation, child: child);
        },
        transitionDuration: const Duration(milliseconds: 1000),
      ),
    );
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        width: double.infinity,
        height: double.infinity,
        // This gradient matches your image perfectly
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            colors: [
              Color(0xFF8BC34A),
              Color(0xFF2E7D32),
            ], // Light to dark green
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
          ),
        ),
        // Wrap the content in the animation
        child: ScaleTransition(
          scale: _scaleAnimation,
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              // 1. The Leaf Icon
              const Icon(Icons.eco_rounded, color: Colors.white, size: 80),
              const SizedBox(height: 10),

              // 2. The "AGRICHECK" text with outline
              // This Stack places outlined text behind white text
              Stack(
                children: [
                  // The outline/shadow
                  Text(
                    'AGRICHECK',
                    style: TextStyle(
                      fontSize: 38,
                      fontWeight: FontWeight.w900,
                      foreground: Paint()
                        ..style = PaintingStyle.stroke
                        ..strokeWidth = 5
                        ..color = Colors.green.shade900, // Dark green outline
                    ),
                  ),
                  // The white text on top
                  const Text(
                    'AGRICHECK',
                    style: TextStyle(
                      fontSize: 38,
                      fontWeight: FontWeight.w900,
                      color: Colors.white,
                      letterSpacing: 1.2,
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 8),

              // 3. The Subtitle
              const Text(
                'Smart Crop Disease Identifier',
                style: TextStyle(
                  color: Colors.black87, // Dark text for contrast
                  fontSize: 15,
                  fontWeight: FontWeight.w500,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
