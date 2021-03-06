#pragma once

#include <armadillo>    // column-major (d x N)
#include <string>

arma::mat sigmoid(const arma::mat& x);
arma::mat softmax(const arma::mat& z);
arma::mat oneHotEncode(const arma::mat& y, int c);
arma::mat oneHotDecode(const arma::mat& OHX);


class Learner {
protected: arma::mat w;
    std::string type;   // regressor, classifier
public:
    Learner(const arma::mat& w0);
    virtual ~Learner() {}
    virtual double computeLoss(const arma::mat& X, const arma::mat& y) = 0;
    virtual arma::mat computeGrad(const arma::mat& X, const arma::mat& y) = 0;
    void update(const arma::mat& X, const arma::mat& y, double learningRate);
    virtual arma::mat predict(const arma::mat& X) = 0;
    arma::mat getWeight() const;
    void setWeight(const arma::mat& w);
};


class LeastSquare: public Learner {
public:
    LeastSquare(const arma::mat& w0);
    virtual double computeLoss(const arma::mat& X, const arma::mat& y);
    virtual arma::mat computeGrad(const arma::mat& X, const arma::mat& y);
    virtual arma::mat predict(const arma::mat& X);
};

class Logistic: public Learner {
public:
    Logistic(const arma::mat& w0);
    virtual double computeLoss(const arma::mat& X, const arma::mat& y);
    virtual arma::mat computeGrad(const arma::mat& X, const arma::mat& y);
    virtual arma::mat predict(const arma::mat& X);
};

// Todo
class Softmax: public Learner {
public:
    Softmax(const arma::mat& w0);
    arma::mat computeProbability(const arma::mat& X);
    virtual double computeLoss(const arma::mat& X, const arma::mat& y);
    virtual arma::mat computeGrad(const arma::mat& X, const arma::mat& y);
    virtual arma::mat predict(const arma::mat& X);
}; 
