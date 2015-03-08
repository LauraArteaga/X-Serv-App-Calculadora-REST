#!/usr/bin/python

import webapp


def extractBody(request, method):
    if (method == "PUT"):
        body = request.split()[-1]
    else:
        body = ""
    return body


def identifyOperation(body):
    if (len(body.split("+")) == 2):
        return "+"
    elif (len(body.split("-")) == 2):
        return "-"
    elif (len(body.split("*")) == 2):
        return "*"
    elif (len(body.split("/")) == 2):
        return "/"
    else:
        return None


def extractOperands(body, operation):
    try:
        num1 = float(body.split(operation)[0])
        num2 = float(body.split(operation)[1])
        operands = (num1, num2)
        return operands
    except ValueError:
        return None


def calculator(operation, operands):
    (num1, num2) = operands
    if (operation == "+"):
        result = num1 + num2
    elif (operation == "-"):
        result = num1 - num2
    elif (operation == "*"):
        result = num1 * num2
    elif (operation == "/"):
        result = num1 / num2
    return result


class calRest(webapp.webApp):

    def parse(self, request):
        method = request.split()[0]
        attribute = request.split()[1][1:]
        body = extractBody(request, method)
        return (method, attribute, body)

    def process(self, parsedRequest):
        if not parsedRequest:
            return("400 Bad Request", "<html><body><h1>ERROR</h1>" +
                   "</body></html>")
        (method, attribute, body) = parsedRequest
        if (method == "GET"):
            operation = identifyOperation(self.storedBody)
            if operation is None:
                return("400 Bad Request", "<html><body><h1>"
                       "ERROR: Debe introducir una operacion"
                       "</h1>" + "</body></html>")
            operands = extractOperands(self.storedBody, operation)
            if operands is None:
                return("400 Bad Request", "<html><body><h1>"
                       "ERROR: Debe introducir dos numeros para operar"
                       "</h1>" + "</body></html>")
            result = calculator(operation, operands)
            num1 = str(operands[0])
            num2 = str(operands[1])
            httpCode = "200 OK"
            htmlBody = num1 + operation + num2 + " = " + str(result)

        elif (method == "PUT"):
            self.storedBody = body
            httpCode = "200 OK"
            htmlBody = body + " OK!"

        return(httpCode, "<html><body><h1>" + htmlBody + "</h1>" +
               "</body></html>")

if __name__ == "__main__":
    calRest = calRest("localhost", 1234)
