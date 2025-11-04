import 'package:dio/dio.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

class ApiService {
  final Dio _dio = Dio(BaseOptions(
    baseUrl: 'http://192.168.1.11', // ⚠️ change to your PC's LAN IP if testing on phone
  ));

  final _storage = const FlutterSecureStorage();

  Future<String> login(String email, String password) async {
    final res = await _dio.post('/auth/login', data: {
      'email': email,
      'password': password,
    });

    final token = res.data['access_token'] as String;
    await _storage.write(key: 'jwt', value: token);
    _dio.options.headers['Authorization'] = 'Bearer $token';
    return token;
  }

  Future<Map<String, dynamic>> getMe() async {
    final token = await _storage.read(key: 'jwt');
    if (token == null) throw Exception('Not logged in');
    _dio.options.headers['Authorization'] = 'Bearer $token';
    final res = await _dio.get('/users/me');
    return res.data;
  }
  Future<Map<String, dynamic>> register({
  required String name,
  required String email,
  required String password,
}) async {
  final res = await _dio.post('/auth/register', data: {
    'name': name,
    'email': email,
    'password': password,
  });
  return res.data as Map<String, dynamic>;
}

}
