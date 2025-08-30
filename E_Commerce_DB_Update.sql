-- =============================================
-- Create Database
-- =============================================
CREATE DATABASE POLOSHOP_DB_1 CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE POLOSHOP_DB_1;

-- =============================================
-- REFERENCE TABLES
-- =============================================

CREATE TABLE IF NOT EXISTS UserType (
    Id BIGINT AUTO_INCREMENT PRIMARY KEY,
    UserType VARCHAR(50) NOT NULL,
    CreatedDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    CreatedBy BIGINT
);

CREATE TABLE IF NOT EXISTS UserStatus (
    Id BIGINT AUTO_INCREMENT PRIMARY KEY,
    Status VARCHAR(10) NOT NULL,
    CreatedDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    CreatedBy BIGINT,
    UpdatedDate DATETIME,
    UpdatedBy BIGINT
);

CREATE TABLE IF NOT EXISTS Country (
    Id BIGINT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    CountryCode VARCHAR(5) NOT NULL UNIQUE,
    CreatedDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    CreatedBy BIGINT,
    UpdatedDate DATETIME,
    UpdatedBy BIGINT
);

CREATE TABLE IF NOT EXISTS Currency (
    Id BIGINT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(10) NOT NULL,
    CountryId BIGINT,
    CurrencyCode VARCHAR(10) NOT NULL UNIQUE,
    CreatedDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    CreatedBy BIGINT,
    FOREIGN KEY (CountryId) REFERENCES Country(Id)
);

CREATE TABLE IF NOT EXISTS Region (
    Id BIGINT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    RegionCode VARCHAR(10) UNIQUE,
    CountryId BIGINT NOT NULL,
    CreatedDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    CreatedBy BIGINT,
    FOREIGN KEY (CountryId) REFERENCES Country(Id)
);

CREATE TABLE IF NOT EXISTS AddressType (
    Id BIGINT AUTO_INCREMENT PRIMARY KEY,
    Type VARCHAR(100) UNIQUE,
    CreatedDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    CreatedBy BIGINT
);

CREATE TABLE IF NOT EXISTS CategoryType (
    Id BIGINT AUTO_INCREMENT PRIMARY KEY,
    Category VARCHAR(100) NOT NULL ,
    CreatedDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    CreatedBy BIGINT
);

CREATE TABLE IF NOT EXISTS Brand (
    Id BIGINT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL UNIQUE,
    CreatedDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    CreatedBy BIGINT
);

CREATE TABLE IF NOT EXISTS DeliveryMode (
    Id BIGINT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL UNIQUE,
    CreatedDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    CreatedBy BIGINT
);

CREATE TABLE IF NOT EXISTS Status (
    Id BIGINT AUTO_INCREMENT PRIMARY KEY,
    Status VARCHAR(50) NOT NULL,
    CreatedDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    CreatedBy BIGINT
);

CREATE TABLE IF NOT EXISTS API (
    Id BIGINT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    `Key` VARCHAR(500) NOT NULL,
    CreatedDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    CreatedBy BIGINT
);

CREATE TABLE IF NOT EXISTS PaymentMethod (
    Id BIGINT AUTO_INCREMENT PRIMARY KEY,
    Method VARCHAR(100) NOT NULL,
    APIKeyId BIGINT,
    CreatedDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    CreatedBy BIGINT,
    FOREIGN KEY (APIKeyId) REFERENCES API(Id)
);

CREATE TABLE IF NOT EXISTS Sender (
    Id BIGINT AUTO_INCREMENT PRIMARY KEY,
    SenderAddress VARCHAR(255) NOT NULL,
    CreatedDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    CreatedBy BIGINT
);

CREATE TABLE IF NOT EXISTS NotificationType (
    Id BIGINT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL UNIQUE,
    CreatedDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    CreatedBy BIGINT
);

CREATE TABLE IF NOT EXISTS NotificationTemplate (
    Id BIGINT AUTO_INCREMENT PRIMARY KEY,
    Message TEXT NOT NULL,
    Subject VARCHAR(200),
    IsActive BOOLEAN,
    CreatedDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    CreatedBy BIGINT
);

CREATE TABLE IF NOT EXISTS GeneralSetup (
    Id BIGINT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Value INT,
    Description VARCHAR(50),
    CreatedDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    CreatedBy BIGINT
);

-- =============================================
-- MAIN ENTITY TABLES
-- =============================================

CREATE TABLE IF NOT EXISTS Users (
    Id BIGINT AUTO_INCREMENT PRIMARY KEY,
    FirstName VARCHAR(100) NOT NULL,
    LastName VARCHAR(100) NOT NULL,
    OtherName VARCHAR(100),
    Email VARCHAR(255) NOT NULL UNIQUE,
    PhoneNo VARCHAR(20) UNIQUE,
    UserTypeId BIGINT NOT NULL,
    UserStatusId BIGINT NOT NULL,
    PasswordHash BLOB NOT NULL,
    LastLoginDate DATETIME,
    FailedLoginAttempts INT DEFAULT 0,
    CreatedDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    CreatedBy BIGINT,
    UpdatedDate DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UpdatedBy BIGINT,
    FOREIGN KEY (UserTypeId) REFERENCES UserType(Id),
    FOREIGN KEY (UserStatusId) REFERENCES UserStatus(Id)
);

CREATE TABLE IF NOT EXISTS Address (
    Id BIGINT AUTO_INCREMENT PRIMARY KEY,
    UserId BIGINT NOT NULL,
    CountryId BIGINT NOT NULL,
    RegionId BIGINT NOT NULL,
    City VARCHAR(200),
    AddressTypeId BIGINT NOT NULL,
    DigitalAddress VARCHAR(100),
    StreetName VARCHAR(200),
    CreatedDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    CreatedBy BIGINT,
    UpdatedDate DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UpdatedBy BIGINT,
    IsDefault BOOLEAN,
    FOREIGN KEY (UserId) REFERENCES Users(Id),
    FOREIGN KEY (CountryId) REFERENCES Country(Id),
    FOREIGN KEY (RegionId) REFERENCES Region(Id)
);

CREATE TABLE IF NOT EXISTS Product (
    Id BIGINT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(200) NOT NULL,
    Description TEXT,
    StatusId BIGINT NOT NULL,
    CategoryId BIGINT NOT NULL,
    BrandId BIGINT NOT NULL,
    Price DECIMAL(18,2) NOT NULL,
    CreatedDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    CreatedBy BIGINT,
    UpdatedDate DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UpdatedBy BIGINT,
    FOREIGN KEY (StatusId) REFERENCES Status(Id),
    FOREIGN KEY (CategoryId) REFERENCES CategoryType(Id),
    FOREIGN KEY (BrandId) REFERENCES Brand(Id)
);

CREATE TABLE IF NOT EXISTS ProductDocument (
    Id BIGINT AUTO_INCREMENT PRIMARY KEY,
    ProductId BIGINT,
    FilePath VARCHAR(500) NOT NULL,
    CreatedDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    CreatedBy BIGINT,
    UpdatedDate DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UpdatedBy BIGINT,
    FOREIGN KEY (ProductId) REFERENCES Product(Id)
);

CREATE TABLE IF NOT EXISTS ProductVariant (
    Id BIGINT AUTO_INCREMENT PRIMARY KEY,
    ProductId BIGINT NOT NULL,
    SKU VARCHAR(100) UNIQUE,
    Attributes JSON,
    Price DECIMAL(18,3) NOT NULL,
    FOREIGN KEY (ProductId) REFERENCES Product(Id)
);

CREATE TABLE IF NOT EXISTS Cart (
    Id BIGINT AUTO_INCREMENT PRIMARY KEY,
    UserId BIGINT NOT NULL,
    StatusId BIGINT NOT NULL,
    CreatedDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    CreatedBy BIGINT,
    UpdatedDate DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UpdatedBy BIGINT,
    FOREIGN KEY (UserId) REFERENCES Users(Id),
    FOREIGN KEY (StatusId) REFERENCES Status(Id)
);

CREATE TABLE IF NOT EXISTS CartItem (
    Id BIGINT AUTO_INCREMENT PRIMARY KEY,
    ProductId BIGINT NOT NULL,
    CartId BIGINT NOT NULL,
    Quantity BIGINT NOT NULL DEFAULT 1,
    CreatedDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    CreatedBy BIGINT,
    UpdatedDate DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UpdatedBy BIGINT,
    FOREIGN KEY (ProductId) REFERENCES Product(Id),
    FOREIGN KEY (CartId) REFERENCES Cart(Id)
);

CREATE TABLE IF NOT EXISTS Orders (
    Id BIGINT AUTO_INCREMENT PRIMARY KEY,
    UserId BIGINT NOT NULL,
    StatusId BIGINT NOT NULL,
    CartId BIGINT,
    Amount DECIMAL(18,3) NOT NULL,
    CreatedDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    CreatedBy BIGINT,
    UpdatedDate DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UpdatedBy BIGINT,
    FOREIGN KEY (CartId) REFERENCES Cart(Id),
    FOREIGN KEY (UserId) REFERENCES Users(Id),
    FOREIGN KEY (StatusId) REFERENCES Status(Id)
);

CREATE TABLE IF NOT EXISTS Transactions (
    Id BIGINT AUTO_INCREMENT PRIMARY KEY,
    PaymentModeId BIGINT NOT NULL,
    OrderId BIGINT,
    StatusId BIGINT,
    Amount DECIMAL(18,3),
    CurrencyId BIGINT,
    CreatedDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    CreatedBy BIGINT,
    UpdatedDate DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UpdatedBy BIGINT,
    FOREIGN KEY (StatusId) REFERENCES Status(Id),
    FOREIGN KEY (CurrencyId) REFERENCES Currency(Id),
    FOREIGN KEY (OrderId) REFERENCES Orders(Id),
    FOREIGN KEY (PaymentModeId) REFERENCES PaymentMethod(Id)
);

CREATE TABLE IF NOT EXISTS OrderStatusHistory (
    Id BIGINT AUTO_INCREMENT PRIMARY KEY,
    OrderId BIGINT NOT NULL,
    StatusId BIGINT NOT NULL,
    ChangedDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    ChangedBy BIGINT,
    UpdatedDate DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UpdatedBy BIGINT,
    FOREIGN KEY (OrderId) REFERENCES Orders(Id),
    FOREIGN KEY (StatusId) REFERENCES Status(Id)
);

CREATE TABLE IF NOT EXISTS SavedItem (
    Id BIGINT AUTO_INCREMENT PRIMARY KEY,
    ProductId BIGINT NOT NULL,
    UserId BIGINT NOT NULL,
    CreatedDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    CreatedBy BIGINT,
    UpdatedDate DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UpdatedBy BIGINT,
    FOREIGN KEY (ProductId) REFERENCES Product(Id),
    FOREIGN KEY (UserId) REFERENCES Users(Id)
);

CREATE TABLE IF NOT EXISTS Review (
    Id BIGINT AUTO_INCREMENT PRIMARY KEY,
    ProductId BIGINT NOT NULL,
    UserId BIGINT NOT NULL,
    Rating INT CHECK (Rating >= 1 AND Rating <= 5),
    Subject VARCHAR(200),
    Message TEXT,
    CreatedDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    CreatedBy BIGINT,
    FOREIGN KEY (ProductId) REFERENCES Product(Id),
    FOREIGN KEY (UserId) REFERENCES Users(Id)
);

CREATE TABLE IF NOT EXISTS Warehouse (
    Id BIGINT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100),
    AddressId BIGINT NOT NULL,
    CreatedDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    CreatedBy BIGINT,
    UpdatedDate DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UpdatedBy BIGINT,
    FOREIGN KEY (AddressId) REFERENCES Address(Id)
);

CREATE TABLE IF NOT EXISTS WarehouseStock (
    Id BIGINT AUTO_INCREMENT PRIMARY KEY,
    WarehouseId BIGINT NOT NULL,
    ProductVariantId BIGINT NOT NULL,
    Quantity INT NOT NULL,
    CreatedDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    CreatedBy BIGINT,
    UpdatedDate DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UpdatedBy BIGINT,
    FOREIGN KEY (WarehouseId) REFERENCES Warehouse(Id),
    FOREIGN KEY (ProductVariantId) REFERENCES ProductVariant(Id)
);

CREATE TABLE IF NOT EXISTS InventoryActionType (
    Id BIGINT AUTO_INCREMENT PRIMARY KEY,
    Code VARCHAR(5) NOT NULL UNIQUE,
    Name VARCHAR(50) NOT NULL,
    CreatedDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    CreatedBy BIGINT
);

CREATE TABLE IF NOT EXISTS Reason (
    Id BIGINT AUTO_INCREMENT PRIMARY KEY,
    Code VARCHAR(50) NOT NULL UNIQUE,
    Description VARCHAR(255) NOT NULL,
    ActionTypeId BIGINT NOT NULL,
    CreatedDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    CreatedBy BIGINT,
    FOREIGN KEY (ActionTypeId) REFERENCES InventoryActionType(Id)
);

CREATE TABLE IF NOT EXISTS InventoryTransaction (
    Id BIGINT AUTO_INCREMENT PRIMARY KEY,
    WarehouseId BIGINT NOT NULL,
    ProductVariantId BIGINT NOT NULL,
    QuantityChange INT NOT NULL,
    ReasonId BIGINT NOT NULL,
    ReferenceId BIGINT NULL,
    CreatedDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    CreatedBy BIGINT,
    FOREIGN KEY (WarehouseId) REFERENCES Warehouse(Id),
    FOREIGN KEY (ProductVariantId) REFERENCES ProductVariant(Id),
    FOREIGN KEY (ReasonId) REFERENCES Reason(Id),
    CHECK (QuantityChange <> 0)
);

CREATE TABLE IF NOT EXISTS Delivery (
    Id BIGINT AUTO_INCREMENT PRIMARY KEY,
    TrackingNumber VARCHAR(50) NOT NULL,
    DeliveryModeId BIGINT NOT NULL,
    OrderId BIGINT NOT NULL,
    StatusId BIGINT NOT NULL,
    AddressId BIGINT NOT NULL,
    DispatchDate DATETIME,
    DeliveryDate DATETIME,
    CreatedDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    CreatedBy BIGINT,
    UpdatedDate DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UpdatedBy BIGINT,
    FOREIGN KEY (AddressId) REFERENCES Address(Id),
    FOREIGN KEY (DeliveryModeId) REFERENCES DeliveryMode(Id),
    FOREIGN KEY (OrderId) REFERENCES Orders(Id),
    FOREIGN KEY (StatusId) REFERENCES Status(Id)
);

CREATE TABLE IF NOT EXISTS PickupStation (
    Id BIGINT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100),
    AddressId BIGINT NOT NULL,
    IsWarehouse BOOLEAN,
    CreatedDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    CreatedBy BIGINT,
    UpdatedDate DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UpdatedBy BIGINT,
    FOREIGN KEY (AddressId) REFERENCES Address(Id)
);

CREATE TABLE IF NOT EXISTS Notification (
    Id BIGINT AUTO_INCREMENT PRIMARY KEY,
    NotificationTypeId BIGINT NOT NULL,
    NotificationTemplateId BIGINT NOT NULL,
    Message TEXT,
    Subject VARCHAR(300),
    SenderId BIGINT NOT NULL,
    Recipient BIGINT NOT NULL,
    CreatedDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    CreatedBy BIGINT,
    FOREIGN KEY (NotificationTemplateId) REFERENCES NotificationTemplate(Id),
    FOREIGN KEY (Recipient) REFERENCES Users(Id),
    FOREIGN KEY (NotificationTypeId) REFERENCES NotificationType(Id),
    FOREIGN KEY (SenderId) REFERENCES Sender(Id)
);




-- =============================================
-- SAMPLE DATA INSERTS (MySQL)
-- =============================================

-- User Types
INSERT INTO UserType (UserType, CreatedBy) VALUES
('Customer', 1),
('Admin', 1),
('Vendor', 1);

-- User Statuses
INSERT INTO UserStatus (Status, CreatedBy) VALUES
('Active', 1),
('Inactive', 1),
('Suspended', 1);

-- Countries
INSERT INTO Country (Name, CountryCode, CreatedBy) VALUES
('Ghana', 'GH', 1),
('Nigeria', 'NG', 1),
('United States', 'US', 1);

-- Regions
INSERT INTO Region (Name, RegionCode, CountryId, CreatedBy) VALUES
('Ashanti Region', 'AS', 1, 1),
('Ahafo Region', 'AF', 1, 1),
('Bono Region', 'BO', 1, 1),
('Bono East Region', 'BE', 1, 1),
('Central Region', 'CE', 1, 1),
('Eastern Region', 'EA', 1, 1),
('Greater Accra Region', 'GA', 1, 1),
('North East Region', 'NE', 1, 1),
('Northern Region', 'NO', 1, 1),
('Oti Region', 'OT', 1, 1),
('Savannah Region', 'SV', 1, 1),
('Upper East Region', 'UE', 1, 1),
('Upper West Region', 'UW', 1, 1),
('Volta Region', 'TV', 1, 1),
('Western Region', 'WE', 1, 1),
('Western North Region', 'WN', 1, 1);



-- Address Types
INSERT INTO AddressType (Type, CreatedBy) VALUES
('Home', 1),
('Work', 1),
('Billing', 1);

-- Statuses
INSERT INTO Status (Status, CreatedBy) VALUES
('Active', 1),
('Inactive', 1),
('Discontinued', 1),
('In Stock', 1),
('Out of Stock', 1),
('Low Stock', 1),
('Pending', 1),
('Processing', 1),
('Shipped', 1),
('Delivered', 1),
('Cancelled', 1),
('In Transit', 1),
('Failed', 1),
('In Cart', 1),
('Checked Out', 1),
('Abandoned', 1);

-- Brands
INSERT INTO Brand (Name, CreatedBy) VALUES
('Apple', 1),
('Nike', 1),
('Addidas', 1),
('Rolex', 1),
('Samsung', 1);

-- Delivery Modes
INSERT INTO DeliveryMode (Name, CreatedBy) VALUES
('Standard Delivery', 1),
('Express Delivery', 1),
('Pickup Station', 1);

-- Notification Types
INSERT INTO NotificationType (Name, CreatedBy) VALUES
('Email', 1),
('SMS', 1),
('Push Notification', 1);

-- Transaction reason types
-- InventoryActionType
INSERT INTO InventoryActionType (Code, Name, CreatedBy) VALUES
('ADD', 'Addition', 1),
('REM', 'Removal', 1);

-- Reason linked to ActionType
INSERT INTO Reason (Code, Description, ActionTypeId, CreatedBy) VALUES
-- ADD actions
('PUR', 'Purchase Order', 1, 1),
('SUP', 'Supplier Stocking', 1, 1),
('ADJ+', 'Positive Adjustment', 1, 1),
-- REM actions
('SAL', 'Customer Sale', 2, 1),
('RET', 'Customer Return', 1, 1),
('DAM', 'Damaged Item', 2, 1),
('CAN', 'Order Cancelled', 1, 1),
('ADJ-', 'Negative Adjustment', 2, 1);




-- Users
CREATE INDEX idx_users_usertype ON Users(UserTypeId);
CREATE INDEX idx_users_userstatus ON Users(UserStatusId);

-- Address
CREATE INDEX idx_address_user ON Address(UserId);
CREATE INDEX idx_address_country ON Address(CountryId);
CREATE INDEX idx_address_region ON Address(RegionId);
CREATE INDEX idx_address_addresstype ON Address(AddressTypeId);

-- Product
CREATE INDEX idx_product_status ON Product(StatusId);
CREATE INDEX idx_product_category ON Product(CategoryId);
CREATE INDEX idx_product_brand ON Product(BrandId);

-- ProductVariant
CREATE INDEX idx_productvariant_product ON ProductVariant(ProductId);

-- Cart & CartItem
CREATE INDEX idx_cart_user ON Cart(UserId);
CREATE INDEX idx_cart_status ON Cart(StatusId);
CREATE INDEX idx_cartitem_cart ON CartItem(CartId);
CREATE INDEX idx_cartitem_product ON CartItem(ProductId);

-- Orders
CREATE INDEX idx_orders_user ON Orders(UserId);
CREATE INDEX idx_orders_status ON Orders(StatusId);
CREATE INDEX idx_orders_cart ON Orders(CartId);

-- Transactions
CREATE INDEX idx_transactions_ord ON Transactions(OrderId);
CREATE INDEX idx_transactions_payment ON Transactions(PaymentModeId);
CREATE INDEX idx_transactions_status ON Transactions(StatusId);
CREATE INDEX idx_transactions_currency ON Transactions(CurrencyId);

-- WarehouseStock
CREATE INDEX idx_warehousestock_wh ON WarehouseStock(WarehouseId);
CREATE INDEX idx_warehousestock_variant ON WarehouseStock(ProductVariantId);

-- InventoryTransaction
CREATE INDEX idx_inventorytransaction_wh ON InventoryTransaction(WarehouseId);
CREATE INDEX idx_inventorytransaction_variant ON InventoryTransaction(ProductVariantId);
CREATE INDEX idx_inventorytransaction_reason ON InventoryTransaction(ReasonId);

-- Delivery
CREATE INDEX idx_delivery_order ON Delivery(OrderId);
CREATE INDEX idx_delivery_status ON Delivery(StatusId);
CREATE INDEX idx_delivery_mode ON Delivery(DeliveryModeId);
CREATE INDEX idx_delivery_address ON Delivery(AddressId);

-- Orders by user and status (for dashboards)
CREATE INDEX idx_orders_user_status ON Orders(UserId, StatusId);

-- Cart items by cart and product (lookup for cart operations)
CREATE INDEX idx_cartitem_cart_product ON CartItem(CartId, ProductId);

-- Transactions filtered by order and status (for reports)
CREATE INDEX idx_transactions_order_status ON Transactions(OrderId, StatusId);

-- Inventory transactions by warehouse and variant (for stock adjustments)
CREATE INDEX idx_inventory_wh_variant ON InventoryTransaction(WarehouseId, ProductVariantId);

-- Ensure SKUs are unique across ProductVariant
ALTER TABLE ProductVariant ADD UNIQUE INDEX uq_productvariant_sku (SKU);

-- Ensure CategoryType names are unique
ALTER TABLE CategoryType ADD UNIQUE INDEX uq_categorytype_category (Category);

-- Ensure PaymentMethod names are unique
ALTER TABLE PaymentMethod ADD UNIQUE INDEX uq_paymentmethod_method (Method);


