from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
from datetime import datetime
# Create the Metadata Object
# metadata_obj = db.MetaData()

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique = True)
    sponcer_id = db.Column(db.String(50), unique = True)
    firstName = db.Column(db.String(100))
    lastName = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(100))
    contactNo = db.Column(db.String(80))
    nominee = db.Column(db.String(100))
    dateTime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    userAdd = db.relationship("UserAddress", uselist=False,back_populates="user")

    def __repr__(self):
        return '<User %r>' % self.firstName

class UserAddress(db.Model):
    __tablename__ = "useraddress"
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(80))
    state = db.Column(db.String(100))
    address = db.Column(db.String(100))
    city = db.Column(db.String(100))
    pinCode = db.Column(db.Integer)
    contactNo = db.Column(db.String(80))
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("User", back_populates="userAdd")
    # users = db.relationship('User')
    dateTime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return '<UserAddress %r>' % self.contactNo

class ReferalUser(db.Model):
    __tablename__ = "referalusers"
    id = db.Column(db.Integer, primary_key=True)
    user_sponcer_id = db.Column(db.String(50), db.ForeignKey('users.sponcer_id'))
    email = db.Column(db.String(120), unique=True)
    dateTime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return '<ReferalUser %r>' % self.email

class Employee(db.Model):
    __tablename__ = "employee"
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique = True)
    image = db.Column(db.String(120))
    name = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    gender = db.Column(db.String(120), unique=True)
    contactNo = db.Column(db.String(80))
    country = db.Column(db.String(80))
    state = db.Column(db.String(100))
    district = db.Column(db.String(100))
    city = db.Column(db.String(100))
    pinCode = db.Column(db.Integer)
    address = db.Column(db.String(100))
    education = db.Column(db.String(100))
    designation = db.Column(db.String(100))
    payBand = db.Column(db.String(100))
    registerNo = db.Column(db.String(100))
    dateTime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return '<Employee %r>' % self.name

class PlanFeature(db.Model):
    __tablename__ = "planfeature"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    plan_id = db.Column(db.Integer, db.ForeignKey('plan.id'))
    dateTime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return '<PlanFeature %r>' % self.name

class Plan(db.Model):
    __tablename__ = "plan"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Integer)
    dateTime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    planfeatures = db.relationship(
        "PlanFeature",
        backref="plan",
        cascade="all, delete, delete-orphan",
        single_parent=True,
    )
    def __repr__(self):
        return '<Plan %r>' % self.name

# inventory start

class Category(db.Model):
    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    active = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Category %r>' % self.name

class Product(db.Model):
    __tablename__ = "product"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description  = db.Column(db.String(100))
    autoReduceStock = db.Column(db.Boolean, default=False)
    freeItem = db.Column(db.Boolean, default=False)
    createdDate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updatedDate = db.Column(db.DateTime, nullable=False)
    # skuNo = db.Column(db.String(100),unique = True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category')
    image = db.Column(db.String(100),unique = True)

    prdprice = db.relationship("ProductPrices", back_populates="product")
    variant = db.relationship("Variants", back_populates="product")
    # variantval = db.relationship("VariantValues", back_populates="product")

    def __repr__(self):
        return '<Product %r>' % self.name

class Variants(db.Model):
    __tablename__ = "variants"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    product = db.relationship('Product',back_populates="variant")

    def __repr__(self):
        return '<Variants %r>' % self.name

class VariantValues(db.Model):
    __tablename__ = "variantValues"
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(100))
    variants_id = db.Column(db.Integer, db.ForeignKey('variants.id'))
    # product = db.relationship('Product',back_populates="variantval")


class ProductPrices(db.Model):
    __tablename__ = "productPrices"
    id = db.Column(db.Integer, primary_key=True)
    sKUNo =  db.Column(db.Integer)
    taxPercent = db.Column(db.Float)
    taxonMRP = db.Column(db.Float)
    mrp = db.Column(db.Integer)
    discountPercent = db.Column(db.Float)
    shippingCharge = db.Column(db.Float)
    ourPrice = db.Column(db.Float)
    stockAvailable = db.Column(db.Boolean, default=False)
    stockOrdered = db.Column(db.Boolean, default=False)

    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    product = db.relationship('Product',back_populates="prdprice")
    #  variantCombinations_id = db.Column(db.Integer, db.ForeignKey('variantCombinations.id'))
    variantValues_id = db.Column(db.Integer, db.ForeignKey('variantValues.id'))
    
    def __repr__(self):
        return '<ProductPrices %r>' % self.sKUNo

class Order(db.Model):
    __tablename__ = "order"
    id = db.Column(db.Integer, primary_key=True)
    orderNo =  db.Column(db.Integer)
    mobileNo =  db.Column(db.Integer)
    postalCode = db.Column(db.String(100))
    area = db.Column(db.String(100))
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    country = db.Column(db.String(100))
    doorNo = db.Column(db.String(100))
    
    totalItems = db.Column(db.Integer)
    totalAmount = db.Column(db.Float)
    totalMRP = db.Column(db.Float)
    totalTax = db.Column(db.Float)
    additionalShippingCharges = db.Column(db.Float)
    totalDiscount = db.Column(db.Float)
    couponDiscount = db.Column(db.Float)
    netAmount = db.Column(db.Float)
    status = db.Column(db.Boolean, default=False)
    paymentType =  db.Column(db.Integer)
    paymentStatus =  db.Column(db.Integer)
    paymentDate = db.Column(db.DateTime, nullable=False)
    comment = db.Column(db.String(100))
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    users = db.relationship('User')

    def __repr__(self):
        return '<Order %r>' % self.orderNo


class OrderDetails(db.Model):
    __tablename__ = "orderDetails"
    id = db.Column(db.Integer, primary_key=True)
    sKUNo =  db.Column(db.Integer)
    offerCode = db.Column(db.String(100))
    mrp = db.Column(db.Float)
    ourPrice = db.Column(db.Float)
    quantity =  db.Column(db.Integer)
    quantityPacked =  db.Column(db.Integer)
    quantityToPacked =  db.Column(db.Integer)
    amount = db.Column(db.Float)
    discount = db.Column(db.Float)
    discountType = db.Column(db.Integer)
    discountAmount = db.Column(db.Float)
    taxPercent = db.Column(db.Integer)
    taxAmount = db.Column(db.Float)
    shippingCharge = db.Column(db.Float)
    lineAmount = db.Column(db.Float)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    order = db.relationship('Order')

    def __repr__(self):
        return '<OrderDetails %r>' % self.sKUNo

class Cart(db.Model):
    __tablename__ = "cart"
    id = db.Column(db.Integer, primary_key=True)
    cartNo =  db.Column(db.Integer)
    date = db.Column(db.DateTime, nullable=False)
    grossAmount = db.Column(db.Float)
    taxAmount = db.Column(db.Float)
    shippingCharge = db.Column(db.Float)
    netAmount = db.Column(db.Float)
    amountPayable = db.Column(db.Float)
    isActive = db.Column(db.Boolean, default=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    users_public_id = db.Column(db.String, db.ForeignKey('users.public_id'))

    product = db.relationship('Product')
    users = db.relationship('User')

    def __repr__(self):
        return '<Cart %r>' % self.cartNo

class WishLists(db.Model):
    __tablename__ = "wishLists"
    id = db.Column(db.Integer, primary_key=True)
    autoProcess = db.Column(db.Boolean, default=False)
    autoProcessDate = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.String(100))
    status = db.Column(db.Boolean, default=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    product = db.relationship('Product')

    def __repr__(self):
        return '<WishLists %r>' % self.autoProcess

class WishListDetails(db.Model):
    __tablename__ = "wishListDetails"
    id = db.Column(db.Integer, primary_key=True)
    sKUNo =  db.Column(db.Integer)
    offerCode = db.Column(db.String(100))
    quantity =  db.Column(db.Integer)

    def __repr__(self):
        return '<WishListDetails %r>' % self.sKUNo

class PaymentDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float)
    provider = db.Column(db.Float)
    isActive = db.Column(db.Boolean, default=False)
    createdDate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updatedDate = db.Column(db.DateTime, nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    # order = db.relationship('Order')




# class Credits(db.Model):
#     __tablename__ = "credits"
#     id = db.Column(db.Integer, primary_key=True)
#     date = db.Column(db.DateTime, nullable=False)
#     credit = db.Column(db.String(100))
#     debit = db.Column(db.String(100))
#     description = db.Column(db.String(100))

#     def __repr__(self):
#         return '<Credits %r>' % self.description

#     def __repr__(self):
#         return '<Credits %r>' % self.description


# inventory End


# class Variants(db.Model):
#     __tablename__ = "variants"
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100))
#     product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
#     def __repr__(self):
#         return '<Variants %r>' % self.name

# class VariantValues(db.Model):
#     __tablename__ = "variantValues"
#     id = db.Column(db.Integer, primary_key=True)
#     value = db.Column(db.String(100))
#     variants_id = db.Column(db.Integer, db.ForeignKey('variants.id'))

#     def __repr__(self):
#         return '<VariantValues %r>' % self.value

# class VariantCombinations(db.Model):
#     __tablename__ = "variantCombinations"
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100))
#     product_id = db.Column(db.Integer, db.ForeignKey('product.id'))

#     def __repr__(self):
#         return '<VariantCombinations %r>' % self.name


# class VariantCombinationValue(db.Model):
#     __tablename__ = "variantCombinationValue"
#     id = db.Column(db.Integer, primary_key=True)
#     value = db.Column(db.String(100))
#     variants_id = db.Column(db.Integer, db.ForeignKey('variants.id'))
#     variantValues_id = db.Column(db.Integer, db.ForeignKey('variantValues.id'))
#     variantCombinations_id = db.Column(db.Integer, db.ForeignKey('variantCombinations.id'))

#     def __repr__(self):
#         return '<VariantCombinationValue %r>' % self.value



# class Payment(db.Model):
#     __tablename__ = "payment"
#     id = db.Column(db.Integer, primary_key=True)
#     # public_id = db.Column(db.String(50), unique = True)
#     paymetType = db.Column(db.String(100))
#     dateTime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#     amount = db.Column(db.String(100))
#     transectionId = db.Column(db.String(100))
#     status = db.Column(db.String(100))
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

#     def __repr__(self):
#         return '<Payment %r>' % self.paymetType


# class Vendors(db.Model):
#     __tablename__ = "vendors"
#     id = db.Column(db.Integer, primary_key=True)
#     storeName = db.Column(db.String(100))
#     emailId = db.Column(db.String(100))
#     password = db.Column(db.String(100))
#     mobileNo = db.Column(db.Integer)
#     postalCode = db.Column(db.String(100))
#     area = db.Column(db.String(100))
#     city = db.Column(db.String(100))
#     state = db.Column(db.String(100))
#     country = db.Column(db.String(100))
#     createdDate = db.Column(db.DateTime, nullable=False)
#     doorNo = db.Column(db.String(100))
#     domainName = db.Column(db.String(100))
#     active = db.Column(db.Boolean, default=False)

#     def __repr__(self):
#         return '<Vendors %r>' % self.storeName

# class VendorContacts(db.Model):
#     __tablename__ = "vendorContacts"
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100))
#     emailId = db.Column(db.String(100))
#     mobileNo = db.Column(db.Integer)
#     designation = db.Column(db.String(100))
#     active = db.Column(db.Boolean, default=False)

#     def __repr__(self):
#         return '<Vendors %r>' % self.name

# class SubCategory(db.Model):
#     __tablename__ = "subCategory"
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100))
#     noOfProduct = db.Column(db.Integer)
#     active = db.Column(db.Boolean, default=False)
#     category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
#     category = db.relationship('Category')

#     def __repr__(self):
#         return '<SubCategory %r>' % self.name


# class TaxDetail(db.Model):
#     __tablename__ = "taxDetail"
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100))
#     fromDate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#     toDate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#     taxPercent = db.Column(db.Float)

#     def __repr__(self):
#         return '<TaxDetail %r>' % self.name



# class Offer(db.Model):
#     __tablename__ = "offer"
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(100))
#     description = db.Column(db.String(100))
#     fromDate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#     toDate = db.Column(db.DateTime, nullable=False)
#     publishDate = db.Column(db.DateTime, nullable=False)
#     offerCode = db.Column(db.String(100))
#     offerType = db.Column(db.String(100))
#     targrtAmount = db.Column(db.Float)
#     targrtOfferType = db.Column(db.Integer)
#     discountAmount = db.Column(db.Float)
#     mrp = db.Column(db.Float)
#     ourPrice = db.Column(db.Float)

#     def __repr__(self):
#         return '<Offer %r>' % self.title

# class OfferProduct(db.Model):
#     __tablename__ = "offerProduct"
#     id = db.Column(db.Integer, primary_key=True)
#     mrp = db.Column(db.Float)
#     discount = db.Column(db.Float)
#     ourPrice = db.Column(db.Float)
#     isBaseProduct = db.Column(db.Boolean, default=False)

#     def __repr__(self):
#         return '<OfferProduct %r>' % self.name

# class Coupons(db.Model):
#     __tablename__ = "coupons"
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(100))
#     description = db.Column(db.String(100))
#     fromDate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#     toDate = db.Column(db.DateTime, nullable=False)
#     publishDate = db.Column(db.DateTime, nullable=False)
#     couponCode = db.Column(db.String(100))
#     couponValue = db.Column(db.Float)
#     couponValueType = db.Column(db.Integer)
#     applyToAllUsers = db.Column(db.Boolean, default=False)
#     applyToNewUsers = db.Column(db.Boolean, default=False)
#     notLoggedMoreThan = db.Column(db.Integer)

#     def __repr__(self):
#         return '<Coupons %r>' % self.title

# class CartDetails(db.Model):
#     __tablename__ = "cartDetails"
#     id = db.Column(db.Integer, primary_key=True)
#     sKUNo =  db.Column(db.Integer)
#     offerCode = db.Column(db.String(100))
#     mrp = db.Column(db.Float)
#     ourPrice = db.Column(db.Float)
#     quantity =  db.Column(db.Integer)
#     amount = db.Column(db.Float)
#     discount = db.Column(db.Float)
#     discountType = db.Column(db.Integer)
#     discountAmount = db.Column(db.Float)
#     taxPercent = db.Column(db.Integer)
#     taxAmount = db.Column(db.Float)
#     shippingCharge = db.Column(db.Float)
#     lineAmount = db.Column(db.Float)

#     def __repr__(self):
#         return '<CartDetails %r>' % self.sKUNo



# class VariantCombinations(db.Model):
#     __tablename__ = "variantCombinations"
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100))
#     value = db.Column(db.String(100))
#     product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
#     product = db.relationship('Product',back_populates="variantcommb")

#     def __repr__(self):
#         return '<VariantCombinations %r>' % self.name