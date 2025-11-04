import 'dart:io';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'results_page.dart'; // Import the results page

class ScanPage extends StatefulWidget {
  const ScanPage({super.key});

  @override
  State<ScanPage> createState() => _ScanPageState();
}

class _ScanPageState extends State<ScanPage> {
  File? _image;
  final ImagePicker _picker = ImagePicker();
  bool _isScanning = false;

  // Colors from your theme
  Color get _green => const Color(0xFF1B5E20); // Dark Green
  Color get _lightGreen => const Color(0xFF388E3C); // Medium Green
  Color get _bgColor => Colors.grey.shade50;

  Future<void> _pickImageFromCamera() async {
    final XFile? pickedFile = await _picker.pickImage(
      source: ImageSource.camera,
      imageQuality: 80, // Compress image slightly
    );
    if (pickedFile != null) {
      setState(() {
        _image = File(pickedFile.path);
      });
    }
  }

  Future<void> _pickImageFromGallery() async {
    final XFile? pickedFile = await _picker.pickImage(
      source: ImageSource.gallery,
      imageQuality: 80, // Compress image slightly
    );
    if (pickedFile != null) {
      setState(() {
        _image = File(pickedFile.path);
      });
    }
  }

  void _removeImage() {
    setState(() {
      _image = null;
    });
  }

  void _scanImage() {
    if (_image == null) return;

    setState(() => _isScanning = true);

    // --- MOCK SCAN ---
    // Simulate a network request or ML model processing
    Future.delayed(const Duration(seconds: 2), () {
      setState(() => _isScanning = false);

      // On success, navigate to the results page
      Navigator.push(
        context,
        MaterialPageRoute(
          builder: (_) => ResultsPage(scannedImagePath: _image?.path),
        ),
      );
    });
  }

  @override
  Widget build(BuildContext context) {
    // Responsive scaling
    final width = MediaQuery.of(context).size.width;
    final scale = (width / 375).clamp(0.85, 1.25);
    double sp(double v) => v * scale;

    return Scaffold(
      backgroundColor: _bgColor,
      appBar: AppBar(
        title: const Text('Scan Plant'),
        backgroundColor: _bgColor,
        foregroundColor: Colors.black87,
        elevation: 0,
      ),
      body: SingleChildScrollView(
        padding: EdgeInsets.all(sp(16)),
        child: Column(
          children: <Widget>[
            // --- Image Preview ---
            Container(
              height: sp(250),
              width: double.infinity,
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.circular(sp(16)),
                border: Border.all(color: Colors.grey.shade300),
              ),
              child: _image != null
                  ? ClipRRect(
                      borderRadius: BorderRadius.circular(sp(16)),
                      child: Image.file(_image!, fit: BoxFit.cover),
                    )
                  : Center(
                      child: Text(
                        'No image selected.',
                        style: TextStyle(
                          fontSize: sp(14),
                          color: Colors.grey.shade600,
                        ),
                      ),
                    ),
            ),
            SizedBox(height: sp(8)),

            // --- Remove Button ---
            if (_image != null)
              Align(
                alignment: Alignment.centerRight,
                child: TextButton.icon(
                  onPressed: _removeImage,
                  icon: Icon(Icons.close, size: sp(16)),
                  label: Text(
                    'Remove Image',
                    style: TextStyle(fontSize: sp(13)),
                  ),
                  style: TextButton.styleFrom(
                    foregroundColor: Colors.red.shade700,
                  ),
                ),
              ),
            SizedBox(height: sp(16)),

            // --- Selection Buttons ---
            Row(
              children: [
                Expanded(
                  child: _buildPickerCard(
                    context,
                    sp: sp,
                    icon: Icons.camera_alt_rounded,
                    label: 'Take Photo',
                    onTap: _pickImageFromCamera,
                  ),
                ),
                SizedBox(width: sp(12)),
                Expanded(
                  child: _buildPickerCard(
                    context,
                    sp: sp,
                    icon: Icons.photo_library_rounded,
                    label: 'From Gallery',
                    onTap: _pickImageFromGallery,
                  ),
                ),
              ],
            ),
            SizedBox(height: sp(32)),

            // --- Scan Button ---
            SizedBox(
              width: double.infinity,
              height: sp(50),
              child: ElevatedButton.icon(
                onPressed: _image != null && !_isScanning ? _scanImage : null,
                icon: _isScanning
                    ? const SizedBox.shrink() // Hide icon when loading
                    : Icon(Icons.document_scanner_outlined, size: sp(20)),
                label: Text(
                  _isScanning ? 'Scanning...' : 'Scan Now',
                  style: TextStyle(
                    fontSize: sp(16),
                    fontWeight: FontWeight.w600,
                  ),
                ),
                style: ElevatedButton.styleFrom(
                  backgroundColor: _green,
                  foregroundColor: Colors.white,
                  disabledBackgroundColor: Colors.grey.shade300,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(sp(10)),
                  ),
                ),
              ),
            ),
            if (_isScanning)
              Padding(
                padding: EdgeInsets.only(top: sp(16)),
                child: const CircularProgressIndicator(),
              ),
          ],
        ),
      ),
    );
  }

  // Helper for the selection cards
  Widget _buildPickerCard(
    BuildContext context, {
    required double Function(double) sp,
    required IconData icon,
    required String label,
    required VoidCallback onTap,
  }) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        height: sp(120),
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(sp(12)),
          border: Border.all(color: Colors.grey.shade300),
          boxShadow: [
            BoxShadow(
              color: Colors.black.withOpacity(0.03),
              blurRadius: 10,
              offset: const Offset(0, 4),
            ),
          ],
        ),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(icon, size: sp(40), color: _lightGreen),
            SizedBox(height: sp(12)),
            Text(
              label,
              style: TextStyle(
                fontSize: sp(14),
                fontWeight: FontWeight.w600,
                color: Colors.black87,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
