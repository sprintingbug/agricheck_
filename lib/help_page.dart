import 'package:flutter/material.dart';

class HelpPage extends StatelessWidget {
  const HelpPage({super.key});

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
        title: const Text('Help & Support'),
        backgroundColor: _bgColor,
        foregroundColor: Colors.black87,
        elevation: 0,
      ),
      body: SingleChildScrollView(
        padding: EdgeInsets.all(sp(16)),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            SizedBox(height: sp(16)),
            Icon(Icons.help_outline_rounded, size: sp(80), color: _green),
            SizedBox(height: sp(24)),
            Text(
              'Help & Support',
              style: TextStyle(
                fontSize: sp(24),
                fontWeight: FontWeight.w700,
                color: Colors.black87,
              ),
            ),
            SizedBox(height: sp(24)),
            _buildHelpSection(
              sp: sp,
              title: 'How to use AgriCheck',
              content: '1. Take a photo of your plant\n2. Wait for the scan to complete\n3. View the results and recommendations',
            ),
            SizedBox(height: sp(16)),
            _buildHelpSection(
              sp: sp,
              title: 'Contact Support',
              content: 'Email: support@agricheck.com\nPhone: +1 (555) 123-4567',
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildHelpSection({
    required double Function(double) sp,
    required String title,
    required String content,
  }) {
    return Container(
      width: double.infinity,
      padding: EdgeInsets.all(sp(16)),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(sp(12)),
        border: Border.all(color: Colors.grey.shade200),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            title,
            style: TextStyle(
              fontSize: sp(18),
              fontWeight: FontWeight.w700,
              color: _green,
            ),
          ),
          SizedBox(height: sp(8)),
          Text(
            content,
            style: TextStyle(
              fontSize: sp(15),
              color: Colors.black87,
              height: 1.5,
            ),
          ),
        ],
      ),
    );
  }
}

