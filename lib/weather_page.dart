import 'dart:async';
import 'dart:convert';
// The 'package:' was accidentally combined in the previous version. This is now fixed.
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

// This is the main widget. It's "Stateful" because its contents (like temperature)
// will change after it's built.
class WeatherPage extends StatefulWidget {
  const WeatherPage({super.key});

  @override
  // This line creates the "State" object that manages all the changing data.
  State<WeatherPage> createState() => _WeatherPageState();
}

// This is the State class. ALL your variables and logic must go inside this class.
class _WeatherPageState extends State<WeatherPage> {
  // --- Keys & config ---
  // Your API key for OpenWeatherMap
  final String apiKey = 'f2f3d05900514bd9267bc69a0a2f7d41';
  // This variable holds the name of the city we are currently showing.
  String? _cityName = 'Manila'; // default city

  // --- Weather state variables ---
  // These variables will hold the data we get from the API.
  // They are "nullable" (with a '?') because they are empty until the API call finishes.
  double? temperature;
  int? humidity;
  String? description;
  // This controls the loading spinner.
  bool isLoading = true;
  // This will hold any error messages.
  String? error;

  // --- Search state variables ---
  // This controls the text in the search bar.
  final _searchCtrl = TextEditingController();
  // This is a helper for delaying the search to avoid too many API calls.
  Timer? _debounce;
  // This controls whether the suggestion list is visible.
  bool _showSuggestions = false;
  // This list will hold the city suggestions from the API.
  List<_City> _suggestions = [];

  // --- App Theme Colors ---
  Color get _green => const Color(0xFF1B5E20); // Dark Green
  Color get _cardColor => const Color(0xFFE6F4EA); // Light Green Card
  Color get _bgColor => Colors.grey.shade50; // Light grey background

  @override
  void initState() {
    super.initState();
    // This function is called ONCE when the page first loads.
    // We fetch the weather for the default city.
    fetchWeatherByCityName(_cityName!);
    // We listen for any typing in the search bar.
    _searchCtrl.addListener(_onSearchChanged);
  }

  @override
  void dispose() {
    // This is a cleanup function.
    // It prevents memory leaks when the page is closed.
    _debounce?.cancel();
    _searchCtrl.dispose();
    super.dispose();
  }

  // ------------------- WEATHER API CALL -------------------
  Future<void> fetchWeatherByCityName(String city) async {
    // 1. Show the loading spinner and clear old errors
    setState(() {
      isLoading = true;
      error = null;
      _cityName = city;
    });

    // 2. Build the API URL
    final url =
        'https://api.openweathermap.org/data/2.5/weather?q=$city&appid=$apiKey&units=metric';

    try {
      // 3. Make the network request
      final res = await http.get(Uri.parse(url));

      // 4. Check if the request was successful
      if (res.statusCode == 200) {
        // 5. Parse the JSON data
        final data = json.decode(res.body);
        // 6. Update our state variables with the new data
        setState(() {
          temperature = (data['main']['temp'] as num?)?.toDouble();
          humidity = (data['main']['humidity'] as num?)?.toInt();
          description = (data['weather']?[0]?['description'] as String?) ?? '—';
          isLoading = false; // Hide loading spinner
        });
      } else {
        // Handle API errors (e.g., city not found)
        setState(() {
          error = 'Failed to load weather data (${res.statusCode}).';
          isLoading = false;
        });
      }
    } catch (e) {
      // Handle network errors (e.g., no internet)
      setState(() {
        error = 'Error: $e';
        isLoading = false;
      });
    }
  }

  // ------------------- SEARCH LOGIC -------------------

  // This function is called every time the user types a letter
  void _onSearchChanged() {
    // Wait 350ms after user stops typing to avoid excessive API calls
    _debounce?.cancel();
    _debounce = Timer(const Duration(milliseconds: 350), () {
      final q = _searchCtrl.text.trim();
      if (q.isEmpty) {
        setState(() {
          _suggestions = [];
          _showSuggestions = false;
        });
      } else {
        _fetchCitySuggestions(q); // Go find city suggestions
      }
    });
  }

  // This function calls the Geocoding API to find cities that match the query
  Future<void> _fetchCitySuggestions(String query) async {
    final url =
        'https://api.openweathermap.org/geo/1.0/direct?q=$query&limit=6&appid=$apiKey';
    try {
      final res = await http.get(Uri.parse(url));
      if (res.statusCode == 200) {
        final List list = json.decode(res.body) as List;
        final cities = list.map((e) => _City.fromJson(e)).toList();
        setState(() {
          _suggestions = cities;
          _showSuggestions = cities.isNotEmpty;
        });
      } else {
        setState(() {
          _suggestions = [];
          _showSuggestions = false;
        });
      }
    } catch (_) {
      // If anything fails, just hide the suggestions
      setState(() {
        _suggestions = [];
        _showSuggestions = false;
      });
    }
  }

  // This is called when a user taps a city from the suggestion list
  void _selectCity(_City city) {
    FocusScope.of(context).unfocus(); // Close keyboard
    _searchCtrl.text = city.displayName;
    _showSuggestions = false;
    fetchWeatherByCityName(city.queryParam); // Fetch weather for the new city
  }

  // ------------------- BUILD METHOD -------------------
  // This function builds the UI
  @override
  Widget build(BuildContext context) {
    // This logic makes your UI responsive to different screen sizes
    final width = MediaQuery.of(context).size.width;
    final scale = (width / 375).clamp(0.85, 1.25);
    double sp(double v) => v * scale;

    // This is a reusable border style for the search input
    final inputBorder = OutlineInputBorder(
      borderRadius: BorderRadius.circular(sp(10)),
      borderSide: BorderSide(color: Colors.grey.shade400, width: 1),
    );

    return Scaffold(
      backgroundColor: _bgColor,
      appBar: AppBar(
        title: const Text('Prices & Weather'),
        backgroundColor: _bgColor,
        foregroundColor: Colors.black87,
        elevation: 0,
      ),
      // This allows the user to "pull to refresh"
      body: RefreshIndicator(
        onRefresh: () => fetchWeatherByCityName(_cityName ?? 'Manila'),
        child: SingleChildScrollView(
          physics: const AlwaysScrollableScrollPhysics(),
          padding: EdgeInsets.all(sp(16)),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // ------------------- SEARCH BOX -------------------
              Stack(
                // Stack is used to overlay the suggestions on top of the page
                children: [
                  TextField(
                    controller: _searchCtrl,
                    decoration: InputDecoration(
                      hintText: 'Search city (e.g., Davao, Cebu, Baguio)',
                      prefixIcon: const Icon(Icons.search),
                      suffixIcon: (_searchCtrl.text.isNotEmpty)
                          ? IconButton(
                              icon: const Icon(Icons.clear),
                              onPressed: () {
                                _searchCtrl.clear();
                                setState(() {
                                  _suggestions = [];
                                  _showSuggestions = false;
                                });
                              },
                            )
                          : null,
                      filled: true,
                      fillColor: Colors.white,
                      border: inputBorder,
                      enabledBorder: inputBorder,
                      focusedBorder: inputBorder.copyWith(
                        borderSide: BorderSide(color: _green, width: sp(1.4)),
                      ),
                      contentPadding: EdgeInsets.symmetric(
                        horizontal: sp(12),
                        vertical: sp(12),
                      ),
                    ),
                    onSubmitted: (v) {
                      final q = v.trim();
                      if (q.isNotEmpty) fetchWeatherByCityName(q);
                    },
                    onTap: () {
                      if (_suggestions.isNotEmpty) {
                        setState(() => _showSuggestions = true);
                      }
                    },
                  ),
                  // --- Suggestions Overlay ---
                  // This widget is only shown if _showSuggestions is true
                  if (_showSuggestions)
                    Positioned(
                      top: sp(54), // Position it below the search bar
                      left: 0,
                      right: 0,
                      child: Material(
                        elevation: 4,
                        borderRadius: BorderRadius.circular(sp(10)),
                        child: ConstrainedBox(
                          constraints: BoxConstraints(maxHeight: sp(220)),
                          child: ListView.separated(
                            shrinkWrap: true,
                            itemCount: _suggestions.length,
                            separatorBuilder: (_, __) =>
                                Divider(height: 1, color: Colors.grey.shade200),
                            itemBuilder: (context, i) {
                              final c = _suggestions[i];
                              return ListTile(
                                dense: true,
                                leading: Icon(
                                  Icons.location_on_outlined,
                                  size: sp(20),
                                ),
                                title: Text(
                                  c.displayName,
                                  style: TextStyle(fontSize: sp(14)),
                                ),
                                subtitle: (c.state?.isNotEmpty ?? false)
                                    ? Text(
                                        c.state!,
                                        style: TextStyle(fontSize: sp(12)),
                                      )
                                    : null,
                                onTap: () => setState(() => _selectCity(c)),
                              );
                            },
                          ),
                        ),
                      ),
                    ),
                ],
              ),
              SizedBox(height: sp(20)),

              // --- Palay Prices section ---
              _buildInfoCard(
                sp: sp,
                icon: Icons.grass_rounded,
                title: '🌾 Palay Prices',
                children: [
                  Text(
                    'Average Market Price: ₱20/kg', // Mock data
                    style: TextStyle(fontSize: sp(15), color: Colors.black87),
                  ),
                ],
              ),
              SizedBox(height: sp(16)),

              // --- Weather section ---
              _buildInfoCard(
                sp: sp,
                icon: Icons.wb_sunny_outlined,
                title: '☀️ Weather in ${_cityName ?? "-"}',
                children: [
                  // Show a loading spinner while fetching data
                  if (isLoading)
                    const Center(
                      child: Padding(
                        padding: EdgeInsets.all(12.0),
                        child: CircularProgressIndicator(),
                      ),
                    )
                  // Show an error message if something went wrong
                  else if (error != null)
                    Text(error!, style: const TextStyle(color: Colors.red))
                  // Otherwise, show the weather data
                  else
                    Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          'Temperature: ${temperature?.toStringAsFixed(1)}°C',
                          style: TextStyle(
                            fontSize: sp(15),
                            color: Colors.black87,
                          ),
                        ),
                        Text(
                          'Humidity: ${humidity ?? 0}%',
                          style: TextStyle(
                            fontSize: sp(15),
                            color: Colors.black87,
                          ),
                        ),
                        Text(
                          'Condition: ${description ?? "N/A"}',
                          style: TextStyle(
                            fontSize: sp(15),
                            color: Colors.black87,
                          ),
                        ),
                        SizedBox(height: sp(10)),
                        TextButton.icon(
                          onPressed: () =>
                              fetchWeatherByCityName(_cityName ?? 'Manila'),
                          icon: Icon(Icons.refresh, size: sp(18)),
                          label: Text(
                            'Refresh',
                            style: TextStyle(fontSize: sp(14)),
                          ),
                          style: TextButton.styleFrom(foregroundColor: _green),
                        ),
                      ],
                    ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }

  // This is a helper widget to avoid repeating code for the info cards
  Widget _buildInfoCard({
    required double Function(double) sp,
    required IconData icon,
    required String title,
    required List<Widget> children,
  }) {
    return Container(
      width: double.infinity,
      padding: EdgeInsets.all(sp(16)),
      decoration: BoxDecoration(
        color: _cardColor, // Use the light green card color
        borderRadius: BorderRadius.circular(sp(16)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            title,
            style: TextStyle(
              fontSize: sp(18),
              fontWeight: FontWeight.w700,
              color: Colors.black87,
            ),
          ),
          SizedBox(height: sp(12)),
          ...children,
        ],
      ),
    );
  }
}

// ------------------- DATA MODEL -------------------
// A simple class to parse the city data from the Geocoding API
class _City {
  final String name;
  final String? state;
  final String country;

  _City({required this.name, required this.country, this.state});

  // Formats the city name for display (e.g., "Manila, PH" or "Cebu, Cebu, PH")
  String get displayName => state == null || state!.isEmpty
      ? '$name, $country'
      : '$name, $state, $country';

  // Formats the city name for the weather API query
  String get queryParam => state == null || state!.isEmpty
      ? '$name,$country'
      : '$name,$state,$country';

  // This "factory constructor" builds a _City object from a JSON map
  factory _City.fromJson(Map<String, dynamic> json) => _City(
    name: (json['name'] as String?) ?? '',
    state: json['state'] as String?,
    country: (json['country'] as String?) ?? '',
  );
}
