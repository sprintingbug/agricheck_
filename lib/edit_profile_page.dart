import 'package:flutter/material.dart';

class EditProfilePage extends StatelessWidget {
  const EditProfilePage({super.key});

  final Color _green = const Color(0xFF1B5E20);
  final Color _bgColor = Colors.grey.shade50;

  @override
  Widget build(BuildContext context) {
    final width = MediaQuery.of(context).size.width;
    final scale = (width / 375).clamp(0.85, 1.25);
    double sp(double v) => v * scale;

    return Scaffold(
      backgroundColor: _bgColor,
      appBar: AppBar(
        title: const Text('Edit Profile'),
        backgroundColor: _bgColor,
        foregroundColor: Colors.black87,
        elevation: 0,
      ),
      body: SingleChildScrollView(
        padding: EdgeInsets.all(sp(16)),
        child: Column(
          children: [
            SizedBox(height: sp(32)),
            Icon(Icons.person_outline, size: sp(80), color: _green),
            SizedBox(height: sp(24)),
            Text(
              'Edit Profile',
              style: TextStyle(
                fontSize: sp(24),
                fontWeight: FontWeight.w700,
                color: Colors.black87,
              ),
            ),
            SizedBox(height: sp(8)),
            Text(
              'Profile editing feature coming soon!',
              style: TextStyle(
                fontSize: sp(15),
                color: Colors.grey.shade600,
              ),
              textAlign: TextAlign.center,
            ),
          ],
        ),
      ),
    );
  }
}

