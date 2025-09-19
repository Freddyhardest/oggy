<?php
// code.php
// A simple, CORS-enabled PHP proxy to fetch and return the HTML source of any URL.

// Enable CORS so your frontend (e.g., on GitHub Pages) can access this script.
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST');
header('Access-Control-Allow-Headers: Content-Type');
header('Content-Type: application/json');

// Get the target URL from the query string
$url = $_GET['url'] ?? '';

// Initialize response data
$response = [
    'html' => '',
    'size' => '0 B',
    'time' => '0.00',
    'error' => null
];

// Start timing the request
$startTime = microtime(true);

// Validate the URL
if (empty($url)) {
    $response['error'] = 'No URL provided.';
    echo json_encode($response);
    exit;
}

if (!filter_var($url, FILTER_VALIDATE_URL)) {
    $response['error'] = 'Invalid URL format. Please use http:// or https://';
    echo json_encode($response);
    exit;
}

// Attempt to fetch the content using file_get_contents
$htmlContent = '';

$context = stream_context_create([
    'http' => [
        'timeout' => 30,
        'user_agent' => 'Mozilla/5.0 (compatible; SourceViewer/1.0)'
    ]
]);

$htmlContent = @file_get_contents($url, false, $context);

if ($htmlContent === false) {
    $response['error'] = 'Failed to fetch content. The target server may be unreachable or blocking requests.';
} else {
    // Calculate stats
    $endTime = microtime(true);
    $response['time'] = number_format($endTime - $startTime, 2);
    $response['size'] = formatBytes(strlen($htmlContent));
    
    // Escape the HTML so it can be safely sent as JSON and displayed in the browser
    $response['html'] = htmlspecialchars($htmlContent);
}

// Send the JSON response back to the frontend
echo json_encode($response);

// Helper function to format bytes
function formatBytes($bytes, $precision = 2) {
    $units = ['B', 'KB', 'MB', 'GB'];
    $bytes = max($bytes, 0);
    $pow = floor(($bytes ? log($bytes) : 0) / log(1024));
    $pow = min($pow, count($units) - 1);
    $bytes /= pow(1024, $pow);
    return round($bytes, $precision) . ' ' . $units[$pow];
}
?>
