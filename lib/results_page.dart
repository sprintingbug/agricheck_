import 'dart:io';
import 'package:flutter/material.dart';

class ResultsPage extends StatelessWidget {
  final String? scannedImagePath;
  
  const ResultsPage({super.key, this.scannedImagePath});

  // Colors from your theme
  final Color _green = const Color(0xFF1B5E20); // Dark Green
  final Color _lightGreen = const Color(0xFF388E3C); // Medium Green
  // Changed to const Color to help analyzer
  final Color _bgColor = const Color(0xFFFAFAFA); // Colors.grey.shade50
  final Color _healthyColor = const Color(0xFFE8F5E9); // Light Green BG
  final Color _healthyText = const Color(0xFF1B5E20); // Dark Green Text

  // Mock data for display
  final String diseaseName = 'Healthy';
  final double confidence = 98.7;
  final String recommendation =
      'Your plant appears to be healthy. Continue with your regular watering and fertilization schedule. Monitor for any changes.';

  @override
  Widget build(BuildContext context) {
    // Responsive scaling
    final width = MediaQuery.of(context).size.width;
    final scale = (width / 375).clamp(0.85, 1.25);
    double sp(double v) => v * scale;

    return Scaffold(
      backgroundColor: _bgColor,
      appBar: AppBar(
        title: const Text('Scan Results'),
        backgroundColor: _bgColor,
        foregroundColor: Colors.black87,
        elevation: 0,
      ),
      body: SingleChildScrollView(
        padding: EdgeInsets.all(sp(16)),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // --- Scanned Image Preview ---
            Container(
              height: sp(200),
              width: double.infinity,
              decoration: BoxDecoration(
                color: Colors.black12,
                borderRadius: BorderRadius.circular(sp(16)),
              ),
              child: scannedImagePath != null && scannedImagePath!.isNotEmpty
                  ? ClipRRect(
                      borderRadius: BorderRadius.circular(sp(16)),
                      child: Image.file(
                        File(scannedImagePath!),
                        fit: BoxFit.cover,
                        errorBuilder: (context, error, stackTrace) {
                          return Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              Icon(
                                Icons.error_outline,
                                size: sp(60),
                                color: Colors.black38,
                              ),
                              SizedBox(height: sp(8)),
                              Text(
                                'Failed to load image',
                                style: TextStyle(fontSize: sp(14), color: Colors.black45),
                              ),
                            ],
                          );
                        },
                      ),
                    )
                  : Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Icon(
                          Icons.image_outlined,
                          size: sp(60),
                          color: Colors.black38,
                        ),
                        SizedBox(height: sp(8)),
                        Text(
                          'Scanned Image Preview',
                          style: TextStyle(fontSize: sp(14), color: Colors.black45),
                        ),
                      ],
                    ),
            ),
            SizedBox(height: sp(20)),

            // --- Result Card ---
            _buildSectionTitle(sp: sp, title: 'Result'),
            SizedBox(height: sp(8)),
            Container(
              width: double.infinity,
              padding: EdgeInsets.all(sp(16)),
              decoration: BoxDecoration(
                color: _healthyColor,
                borderRadius: BorderRadius.circular(sp(12)),
                border: Border.all(color: _healthyText.withOpacity(0.5)),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    diseaseName.toUpperCase(),
                    style: TextStyle(
                      fontSize: sp(18),
                      fontWeight: FontWeight.w800,
                      color: _healthyText,
                      letterSpacing: 0.5,
                    ),
                  ),
                  SizedBox(height: sp(4)),
                  Text(
                    'Confidence: ${confidence.toStringAsFixed(1)}%',
                    style: TextStyle(
                      fontSize: sp(15),
                      fontWeight: FontWeight.w600,
                      color: _healthyText.withOpacity(0.8),
                    ),
                  ),
                ],
              ),
            ),
            SizedBox(height: sp(24)),

            // --- Recommendations ---
            _buildSectionTitle(sp: sp, title: 'Recommended Actions'),
            SizedBox(height: sp(8)),
            Text(
              recommendation,
              style: TextStyle(
                fontSize: sp(15),
                height: 1.5,
                color: Colors.black87,
              ),
            ),
            SizedBox(height: sp(32)),

            // --- Action Button ---
            SizedBox(
              width: double.infinity,
              height: sp(50),
              child: ElevatedButton.icon(
                onPressed: () {
                  // Save to reports - in a real app, this would save to a database or local storage
                  ScaffoldMessenger.of(context).showSnackBar(
                    const SnackBar(
                      content: Text('Report saved successfully!'),
                      duration: Duration(seconds: 2),
                    ),
                  );
                  Navigator.pop(context); // Go back to scan page
                },
                icon: Icon(Icons.save_alt_rounded, size: sp(20)),
                label: Text(
                  'Save to Reports',
                  style: TextStyle(fontSize: sp(16)),
                ),
                style: ElevatedButton.styleFrom(
                  backgroundColor: _lightGreen,
                  foregroundColor: Colors.white,
                  elevation: 0,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(sp(12)),
                  ),
                ),
              ),
            ),
            SizedBox(height: sp(12)),
            SizedBox(
              width: double.infinity,
              height: sp(50),
              child: TextButton(
                onPressed: () {
                  Navigator.pop(context); // Go back to scan page
                },
                style: TextButton.styleFrom(
                  foregroundColor: _green,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(sp(12)),
                  ),
                ),
                child: Text('Scan Another', style: TextStyle(fontSize: sp(16))),
              ),
            ),
          ],
        ),
      ),
    );
  }
} // <-- End of ResultsPage class

// Helper for section titles (moved outside class)
Widget _buildSectionTitle({
  required double Function(double) sp,
  required String title,
}) {
  return Text(
    title,
    style: TextStyle(
      fontSize: sp(18),
      fontWeight: FontWeight.w700,
      color: const Color(0xFF1B5E20), // Use const color directly
    ),
  );
}
