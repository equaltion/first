#include "real.h"
#include "httplib.h"
#include "json.hpp"
#include <iostream>
#include <string>

int main() {
    httplib::Server svr;
    
    svr.Get("/", [](const httplib::Request& req, httplib::Response& res) {
        res.set_content("Hello from real server!", "text/plain");
    });
    svr.Post("/use",[](const httplib::Request& req, httplib::Response& res) { 
        
     });

    std::cout << "Server is running at http://localhost:8080" << std::endl;
    svr.listen("localhost", 8080);

    return 0;
}