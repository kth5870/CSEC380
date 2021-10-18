<!DOCTYPE html>
<html>
    <head>
        <title> Test </title>

        <!-- Matomo Tracking Code-->
        <script type="text/javascript">
            var _paq = window._paq = window._pag || [];
            _paq.push(['trackPageView']);
            _paq.push(['enableLinkTracing']);
            (function (){
                var url = "192.168.237.128";
                _paq.push(['setTrackerUrl', url+'matomo.php']);
                _paq.push(['setSiteId', '1']);
                var d=document, g=d.createElement('script'), s=d.getElementByTagName('script'[0]);
                g.type="text/javascript"; g.async=true; g.src=url+'matomo.js'; s.parentNode.insertBefore(g, s);
            })();
        </script>

        <script type="text/javascript">
            function plugin() {
                var length = Document.plugins.length;
                var s = "";
                for (var i = 0; i < length; i++) {
                    s += length[i].name + "<br>"
                }
            document.getElementById("plugins").innerHTML = txt;
            window.onload = plugin;
        </script>

    </head>

    <body>
        <?php
            $referer = isset($_POST['referer']) ? trim($_POST['referer']) : (isset($_SERVER['HTTP_REFERER']) ? base64_encode($_SERVER['HTTP_REFERER']) : false);

            // $referer = $_SERVER["HTTP_REFERER"];
            $ip = $_SERVER["REMOTE_ADDR"];
            $user_agent = $_SERVER["HTTP_USER_AGENT"];

            echo "Referer: " . $referer . "<br>";
            echo "IP Addr: " . $ip . "<br>";
            echo "User-Agent:" . $user_agent . "<br>";
        ?>

        <div id="plugins"></div>
    </body>
</html>
