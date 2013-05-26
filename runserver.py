def run(host, port):
    from application import app
    app.run(host, port, debug=True)

if __name__ == '__main__':
    run(host='localhost', port=5000)
