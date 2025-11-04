import 'package:flutter/material.dart';
import 'splash_page.dart'; 

void main() => runApp(const AgriCheckApp());

class AgriCheckApp extends StatelessWidget {
  const AgriCheckApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      // 2. Set the 'home' property to your SplashPage.
      // This tells Flutter to show this page first.
      home: const SplashPage(),

      // Optional: You can set a theme for your whole app here
      theme: ThemeData(
        primaryColor: const Color(0xFF2E7D32), // Your app's green color
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.green),
        useMaterial3: true,
      ),
    );
  }
}
